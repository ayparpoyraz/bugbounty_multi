from pathlib import Path
from urllib.parse import urlsplit
import subprocess


def feroxbuster_tara():
    program = (
        Path.home()
        / "Downloads"
        / "Feroxbuster"
        / "feroxbuster.exe"
    )

    if not program.is_file():
        print(f"Feroxbuster bulunamadı: {program}")
        return

    hedef = input("Hedef URL (http:// veya https://): ").strip()

    try:
        adres = urlsplit(hedef)
        gecerli = (
            adres.scheme in ("http", "https")
            and adres.hostname is not None
            and not any(karakter.isspace() for karakter in hedef)
        )
    except ValueError:
        gecerli = False

    if not gecerli:
        print("Geçerli bir http:// veya https:// adresi gir.")
        return

    wordlist = Path(
        input("Wordlist dosyasının tam yolu: ").strip().strip('"')
    )

    if not wordlist.is_file():
        print("Wordlist dosyası bulunamadı.")
        return

    try:
        sonuc = subprocess.run(
            [
                str(program),
                "-u", hedef,
                "-w", str(wordlist),
                "--no-recursion",
            ],
            check=False,
        )

        if sonuc.returncode != 0:
            print(f"Feroxbuster hata koduyla tamamlandı: {sonuc.returncode}")

    except OSError as hata:
        print(f"Feroxbuster başlatılamadı: {hata}")


if __name__ == "__main__":
    feroxbuster_tara()