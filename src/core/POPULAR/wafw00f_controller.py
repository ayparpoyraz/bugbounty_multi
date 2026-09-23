from importlib.util import find_spec
from urllib.parse import urlsplit
import subprocess
import sys


def wafw00f_tara():
    if find_spec("wafw00f") is None:
        print("Wafw00f kurulu değil.")
        print("Kurulum komutu: python3 -m pip install wafw00f")
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
                sys.executable,
                "-c",
                "from wafw00f.main import main; main()",
                hedef,
            ],
            check=False,
        )

        if sonuc.returncode != 0:
            print(f"Wafw00f hata koduyla tamamlandı: {sonuc.returncode}")

    except OSError as hata:
        print(f"Wafw00f başlatılamadı: {hata}")


if __name__ == "__main__":
    wafw00f_tara()