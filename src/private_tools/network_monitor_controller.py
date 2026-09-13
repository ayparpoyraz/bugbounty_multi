import argparse
from datetime import datetime
import ipaddress
import os
from pathlib import Path
import socket
import sqlite3
import tempfile
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


console = Console()

def network_monitor():
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
            return ipaddress.ip_address(
                host.split('%')[0]
            ).is_global
        except ValueError:
            return False


    def temporary(executable):
        if not executable:
            return False

        roots = [tempfile.gettempdir()]

        if os.name == 'nt':
            roots.append(
                os.path.join(
                    os.environ.get(
                        'SystemRoot',
                        r'C:\Windows'
                    ),
                    'Temp',
                )
            )
        else:
            roots.extend([
                '/tmp',
                '/var/tmp'
            ])

        try:
            path = Path(executable).resolve()

            for root in roots:
                try:
                    path.relative_to(
                        Path(root).resolve()
                    )

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
            connections = psutil.net_connections(
                kind='inet'
            )

        except (psutil.AccessDenied, OSError) as exc:
            console.print(
                Panel(
                    f'[bold red]Bağlantılar okunamadı[/bold red]\n\n'
                    f'[white]{clean(exc)}[/white]\n\n'
                    f'[yellow]Gerekirse yönetici olarak '
                    f'çalıştırınız.[/yellow]',
                    title='ERROR',
                    border_style='red',
                    box=box.ROUNDED,
                )
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

                name = 'Bilinmiyor'
                executable = ''
                created = None

                if pid is not None:
                    try:
                        process = psutil.Process(pid)

                        created = process.create_time()
                        name = process.name()

                        try:
                            executable = process.exe()

                        except (
                            psutil.AccessDenied,
                            psutil.NoSuchProcess
                        ):
                            pass

                    except (
                        psutil.AccessDenied,
                        psutil.NoSuchProcess
                    ):
                        pass

                cache[pid] = (
                    name,
                    executable,
                    created
                )

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

            now = datetime.now().astimezone().isoformat(
                timespec='seconds'
            )

            flags = []

            if (
                executable
                and public_address(connection.raddr[0])
            ):
                identity = os.path.normcase(
                    os.path.abspath(executable)
                )

                inserted = db.execute(
                    '''
                    INSERT OR IGNORE INTO programs (
                        identity,
                        first_seen
                    )
                    VALUES (?, ?)
                    ''',
                    (
                        identity,
                        now
                    ),
                )

                if inserted.rowcount > 0:
                    flags.append(
                        'İLK GENEL IP BAĞLANTISI GÖZLEMİ'
                    )

            if temporary(executable):
                flags.append(
                    'GEÇİCİ KLASÖR'
                )

            if not executable:
                flags.append(
                    'İŞLEM YOLU OKUNAMADI'
                )

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

            # -----------------------------
            # RICH OUTPUT
            # -----------------------------

            status_style = {
                'ESTABLISHED': 'green',
                'LISTEN': 'cyan',
                'TIME_WAIT': 'yellow',
                'CLOSE_WAIT': 'yellow',
                'SYN_SENT': 'magenta',
                'SYN_RECV': 'magenta',
                'FIN_WAIT1': 'yellow',
                'FIN_WAIT2': 'yellow',
            }.get(
                connection.status,
                'white'
            )

            protocol_style = (
                'cyan'
                if protocol == 'TCP'
                else 'magenta'
            )

            console.print(
                f'[dim]{clean(now)}[/dim] '
                f'[bold blue]PID {pid}[/bold blue] '
                f'[bold white]{clean(name)}[/bold white] '
                f'[dim]│[/dim] '
                f'[{protocol_style}]{protocol}'
                f'[/{protocol_style}] '
                f'[white]{clean(local)}[/white] '
                f'[dim]→[/dim] '
                f'[white]{clean(remote)}[/white] '
                f'[dim]│[/dim] '
                f'[{status_style}]'
                f'{clean(connection.status)}'
                f'[/{status_style}] '
                f'[dim]│[/dim] '
                f'[yellow]{clean(flag_text)}[/yellow]'
            )

            if executable:
                console.print(
                    f'    [dim]└─[/dim] '
                    f'[green]{clean(executable)}[/green]'
                )

            count += 1

        db.commit()

        return current, count


    def main():

        parser = argparse.ArgumentParser(
            description=(
                'Ağ bağlantılarını gözlemle ve '
                'SQLite geçmişine kaydet.'
            )
        )

        parser.add_argument(
            '--db',
            type=Path,
            default=Path(__file__).resolve().with_name(
                'ag_gecmisi.sqlite3'
            ),
        )

        parser.add_argument(
            '--interval',
            type=float,
            default=2,
            help=(
                'Örnekleme aralığı '
                '(saniye, en az 0.2)'
            ),
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
            help=(
                'Geçmişi yerel tarihe göre filtrele: '
                'YYYY-MM-DD'
            ),
        )

        parser.add_argument(
            '--program',
            help='Geçmişte işlem adı içinde ara',
        )

        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help=(
                'Gösterilecek en fazla geçmiş kaydı'
            ),
        )

        args = parser.parse_args()

        # -----------------------------
        # ARGUMENT VALIDATION
        # -----------------------------

        if not 0.2 <= args.interval <= 86400:
            parser.error(
                '--interval 0.2 ile 86400 arasında olmalı'
            )

        if args.limit < 1:
            parser.error(
                '--limit pozitif olmalı'
            )

        if args.date is not None:

            try:
                parsed_date = datetime.strptime(
                    args.date,
                    '%Y-%m-%d'
                )

                if (
                    parsed_date.strftime('%Y-%m-%d')
                    != args.date
                ):
                    raise ValueError

            except ValueError:
                parser.error(
                    '--date YYYY-MM-DD biçiminde olmalı'
                )

        if (
            args.date is not None
            or args.program is not None
        ) and not args.history:

            parser.error(
                '--date ve --program için '
                '--history kullanın'
            )

        db = open_database(args.db)

        try:

            # =============================
            # HISTORY
            # =============================

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
                    WHERE (
                        ? IS NULL
                        OR substr(
                            observed_at,
                            1,
                            10
                        ) = ?
                    )
                    AND (
                        ? IS NULL
                        OR instr(
                            lower(program),
                            lower(?)
                        ) > 0
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

                if not rows:

                    console.print(
                        Panel(
                            '[yellow]'
                            'Eşleşen kayıt bulunamadı.'
                            '[/yellow]',
                            title='HISTORY',
                            border_style='yellow',
                            box=box.ROUNDED,
                        )
                    )

                    return

                table = Table(
                    title='NETWORK HISTORY',
                    box=box.ROUNDED,
                    border_style='cyan',
                    header_style='bold cyan',
                    expand=False,
                )

                table.add_column(
                    'Time',
                    style='dim'
                )

                table.add_column(
                    'PID',
                    style='blue'
                )

                table.add_column(
                    'Program',
                    style='white'
                )

                table.add_column(
                    'Protocol',
                    style='cyan'
                )

                table.add_column(
                    'Remote',
                    style='magenta'
                )

                table.add_column(
                    'Status',
                    style='green'
                )

                table.add_column(
                    'Flags',
                    style='yellow'
                )

                for row in rows:

                    (
                        observed_at,
                        pid,
                        program,
                        protocol,
                        remote,
                        status,
                        flags,
                        executable,
                    ) = row

                    status_style = {
                        'ESTABLISHED': 'green',
                        'LISTEN': 'cyan',
                        'TIME_WAIT': 'yellow',
                        'CLOSE_WAIT': 'yellow',
                    }.get(
                        status,
                        'white'
                    )

                    table.add_row(
                        clean(observed_at),
                        str(pid),
                        clean(program),
                        clean(protocol),
                        clean(remote),
                        (
                            f'[{status_style}]'
                            f'{clean(status)}'
                            f'[/{status_style}]'
                        ),
                        clean(flags),
                    )

                console.print(table)

                return

            # =============================
            # PSUTIL
            # =============================

            try:
                import psutil

            except ImportError:

                console.print(
                    Panel(
                        '[bold red]'
                        'psutil bulunamadı.'
                        '[/bold red]\n\n'
                        '[white]Kurulum:[/white] '
                        '[cyan]'
                        'python3 -m pip install psutil'
                        '[/cyan]',
                        title='DEPENDENCY ERROR',
                        border_style='red',
                        box=box.ROUNDED,
                    )
                )

                raise SystemExit(1)

            # =============================
            # STARTUP
            # =============================

            console.print()

            console.print(
                Panel(
                    '[bold cyan]'
                    'NETWORK WATCHER'
                    '[/bold cyan]\n'
                    '[dim]'
                    'Process & Network Connection Monitor'
                    '[/dim]',
                    title='START',
                    border_style='cyan',
                    box=box.ROUNDED,
                    padding=(1, 2),
                )
            )

            info = Table(
                show_header=False,
                box=None,
                padding=(0, 1),
            )

            info.add_column(
                style='bold cyan',
                width=12
            )

            info.add_column(
                style='white'
            )

            info.add_row(
                'Database',
                str(args.db.resolve())
            )

            info.add_row(
                'Interval',
                f'{args.interval}s'
            )

            info.add_row(
                'Mode',
                (
                    'Single scan'
                    if args.once
                    else 'Continuous'
                )
            )

            console.print(info)

            console.print()

            console.print(
                Panel(
                    '[yellow]'
                    'İşaretler tek başına zararlı yazılım '
                    'kanıtı değildir.'
                    '[/yellow]\n'
                    '[dim]'
                    'İlk gözlem, bu veritabanında ilk kez '
                    'görülmeyi ifade eder.'
                    '[/dim]',
                    title='NOTICE',
                    border_style='yellow',
                    box=box.ROUNDED,
                )
            )

            console.print(
                '[dim]'
                'Durdurmak için '
                '[bold]CTRL + C[/bold]'
                '[/dim]\n'
            )

            previous = set()

            # =============================
            # MAIN LOOP
            # =============================

            while True:

                previous, count = observe(
                    db,
                    psutil,
                    previous,
                )

                if args.once:

                    console.print(
                        Panel(
                            f'[bold green]{count}'
                            f'[/bold green] '
                            'yeni bağlantı/durum '
                            'gözlemi kaydedildi.',
                            title='SCAN COMPLETE',
                            border_style='green',
                            box=box.ROUNDED,
                        )
                    )

                    break

                time.sleep(args.interval)

        except KeyboardInterrupt:

            console.print()

            console.print(
                Panel(
                    '[bold yellow]'
                    'İzleme durduruldu.'
                    '[/bold yellow]',
                    title='STOPPED',
                    border_style='yellow',
                    box=box.ROUNDED,
                )
            )

        finally:
            db.close()


    if __name__ == '__main__':
        main()

if __name__ == '__main__':
    network_monitor()