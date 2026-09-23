from pathlib import Path
from urllib.parse import urlsplit
import subprocess


def httpx_tara():
    program = Path.home() / "Downloads" / "Httpx" / "httpx.exe"

    if not program.is_file():
        print(f"httpx bulunamadı: {program}")
        return

    hedef = input("Hedef URL (örnek: https://example.com): ").strip()

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

    try:
        sonuc = subprocess.run(
            [
                str(program),
                "-u", hedef,
                "-status-code",
                "-title",
                "-web-server",
            ],
            check=False,
        )

        if sonuc.returncode != 0:
            print(f"httpx hata koduyla tamamlandı: {sonuc.returncode}")

    except OSError as hata:
        print(f"httpx başlatılamadı: {hata}")


if __name__ == "__main__":
    httpx_tara()