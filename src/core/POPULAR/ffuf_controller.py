from pathlib import Path
from urllib.parse import urlsplit
import shutil
import subprocess


def ffuf_tara():
    program = shutil.which("ffuf")

    if program is None:
        print("ffuf bulunamadı. Kurulumu ve PATH ayarını kontrol et.")
        return

    hedef = input(
        "Hedef URL (örnek: http://127.0.0.1:8000/FUZZ): "
    ).strip()

    url = urlsplit(hedef)

    if url.scheme not in ("http", "https") or not url.netloc:
        print("Geçerli bir http:// veya https:// adresi gir.")
        return

    if "FUZZ" not in url.path:
        print("URL yolunda FUZZ bulunmalı. Örnek: http://127.0.0.1:8000/FUZZ")
        return

    wordlist = Path(
        input("Wordlist dosyasının tam yolu: ").strip().strip('"')
    )

    if not wordlist.is_file():
        print("Wordlist dosyası bulunamadı.")
        return

    try:
        sonuc = subprocess.run(
            [program, "-u", hedef, "-w", str(wordlist)],
            check=False,
        )

        if sonuc.returncode != 0:
            print(f"ffuf hata koduyla tamamlandı: {sonuc.returncode}")
    except OSError as hata:
        print(f"ffuf başlatılamadı: {hata}")


if __name__ == "__main__":
    ffuf_tara()