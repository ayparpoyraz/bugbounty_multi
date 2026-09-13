import argparse
from datetime import datetime
import ipaddress
import os
from pathlib import Path
import socket
import sqlite3
import tempfile
import time


def clean(value):
    return ''.join(
        c if c.isprintable() else '?'
        for c in str(value)
    )


def endpoint(address):
    if not address:
        return ''

    host, port = address[:2]
    return f'[{host}]:{port}' if ':' in host else f'{host}:{port}'


def public_address(host):
    try:
        return ipaddress.ip_address(host.split('%')[0]).is_global
    except ValueError:
        return False


def temporary(executable):
    if not executable:
        return False

    roots = [tempfile.gettempdir()]

    if os.name == 'nt':
        roots.append(
            os.path.join(
                os.environ.get('SystemRoot', r'C:\Windows'),
                'Temp',
            )
        )
    else:
        roots.extend(['/tmp', '/var/tmp'])

    try:
        path = Path(executable).resolve()

        for root in roots:
            try:
                path.relative_to(Path(root).resolve())
                return True
            except ValueError:
                continue

    except (OSError, RuntimeError):
        return False

    return False


def open_database(path):
    db = sqlite3.connect(path)

    try:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS programs (
                identity TEXT PRIMARY KEY,
                first_seen TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                observed_at TEXT NOT NULL,
                pid INTEGER,
                program TEXT,
                executable TEXT,
                protocol TEXT,
                local_address TEXT,
                remote_address TEXT,
                status TEXT,
                flags TEXT
            );

            CREATE INDEX IF NOT EXISTS events_date
            ON events(observed_at);
        ''')
    except sqlite3.Error:
        db.close()
        raise

    return db


def observe(db, psutil, previous):
    try:
        connections = psutil.net_connections(kind='inet')
    except (psutil.AccessDenied, OSError) as exc:
        print(
            f'Bağlantılar okunamadı: {clean(exc)}. '
            'Gerekirse yönetici olarak çalıştırınız.',
            flush=True,
        )
        return previous, 0

    current = set()
    cache = {}
    count = 0

    for connection in connections:
        if not connection.raddr:
            continue

        pid = connection.pid

        if pid not in cache:
            name, executable, created = 'Bilinmiyor', '', None

            if pid is not None:
                try:
                    process = psutil.Process(pid)
                    created = process.create_time()
                    name = process.name()

                    try:
                        executable = process.exe()
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass

                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass

            cache[pid] = name, executable, created

        name, executable, created = cache[pid]

        protocol = (
            'TCP'
            if connection.type == socket.SOCK_STREAM
            else 'UDP'
        )

        local = endpoint(connection.laddr)
        remote = endpoint(connection.raddr)

        key = (
            pid,
            created,
            protocol,
            local,
            remote,
            connection.status,
        )

        if key in current:
            continue

        current.add(key)

        if key in previous:
            continue

        now = datetime.now().astimezone().isoformat(timespec='seconds')
        flags = []

        if executable and public_address(connection.raddr[0]):
            identity = os.path.normcase(os.path.abspath(executable))

            inserted = db.execute(
                '''
                INSERT OR IGNORE INTO programs (identity, first_seen)
                VALUES (?, ?)
                ''',
                (identity, now),
            )

            if inserted.rowcount > 0:
                flags.append('İLK GENEL IP BAĞLANTISI GÖZLEMİ')

        if temporary(executable):
            flags.append('GEÇİCİ KLASÖR')

        if not executable:
            flags.append('İŞLEM YOLU OKUNAMADI')

        flag_text = ', '.join(flags) or '-'

        db.execute(
            '''
            INSERT INTO events (
                observed_at,
                pid,
                program,
                executable,
                protocol,
                local_address,
                remote_address,
                status,
                flags
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                now,
                pid,
                name,
                executable,
                protocol,
                local,
                remote,
                connection.status,
                flag_text,
            ),
        )

        print(
            clean(
                f'{now} | PID {pid} | {name} | '
                f'{protocol} {local} -> {remote} | '
                f'{connection.status} | {flag_text}'
            ),
            flush=True,
        )

        if executable:
            print('  ' + clean(executable), flush=True)

        count += 1

    db.commit()
    return current, count


def main():
    parser = argparse.ArgumentParser(
        description='Ağ bağlantılarını gözlemle ve SQLite geçmişine kaydet.'
    )

    parser.add_argument(
        '--db',
        type=Path,
        default=Path(__file__).resolve().with_name('ag_gecmisi.sqlite3'),
    )
    parser.add_argument(
        '--interval',
        type=float,
        default=2,
        help='Örnekleme aralığı (saniye, en az 0.2)',
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Bir örnekleme yap ve çık',
    )
    parser.add_argument(
        '--history',
        action='store_true',
        help='Kaydedilmiş olayları göster',
    )
    parser.add_argument(
        '--date',
        help='Geçmişi yerel tarihe göre filtrele: YYYY-MM-DD',
    )
    parser.add_argument(
        '--program',
        help='Geçmişte işlem adı içinde ara',
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Gösterilecek en fazla geçmiş kaydı',
    )

    args = parser.parse_args()

    if not 0.2 <= args.interval <= 86400:
        parser.error('--interval 0.2 ile 86400 arasında olmalı')

    if args.limit < 1:
        parser.error('--limit pozitif olmalı')

    if args.date is not None:
        try:
            parsed_date = datetime.strptime(args.date, '%Y-%m-%d')
            if parsed_date.strftime('%Y-%m-%d') != args.date:
                raise ValueError
        except ValueError:
            parser.error('--date YYYY-MM-DD biçiminde olmalı')

    if (
        args.date is not None or args.program is not None
    ) and not args.history:
        parser.error('--date ve --program için --history kullanın')

    db = open_database(args.db)

    try:
        if args.history:
            rows = db.execute(
                '''
                SELECT
                    observed_at,
                    pid,
                    program,
                    protocol,
                    remote_address,
                    status,
                    flags,
                    executable
                FROM events
                WHERE (? IS NULL OR substr(observed_at, 1, 10) = ?)
                  AND (
                      ? IS NULL
                      OR instr(lower(program), lower(?)) > 0
                  )
                ORDER BY id DESC
                LIMIT ?
                ''',
                (
                    args.date,
                    args.date,
                    args.program,
                    args.program,
                    args.limit,
                ),
            ).fetchall()

            for row in rows:
                print(clean(' | '.join(str(value) for value in row)))

            if not rows:
                print('Eşleşen kayıt bulunamadı.')

            return

        try:
            import psutil
        except ImportError:
            raise SystemExit(
                'Eksik bağımlılık. Kurulum: python -m pip install psutil'
            ) from None

        print(
            f'Ağ Gözcüsü başladı. Veritabanı: {args.db.resolve()}\n'
            'Durdurmak için CTRL + C.'
        )
        print(
            'İşaretler tek başına zararlı yazılım kanıtı değildir. '
            'İlk gözlem, bu veritabanında ilk kez görülmeyi ifade eder.'
        )

        previous = set()

        while True:
            previous, count = observe(db, psutil, previous)

            if args.once:
                print(
                    f'{count} yeni bağlantı/durum gözlemi kaydedildi.'
                )
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print('\nİzleme durduruldu.')
    finally:
        db.close()


if __name__ == '__main__':
    main()
