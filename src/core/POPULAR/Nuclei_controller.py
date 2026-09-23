from pathlib import Path
from urllib.parse import urlsplit
import subprocess


def nuclei_tara():
    program = (
        Path.home()
        / "Downloads"
        / "nuclei_3.11.1_windows_amd64 (1)"
        / "nuclei.exe"
    )

    # Dosyanın bulunduğunu kontrol eder.
    if not program.is_file():
        print(f"Nuclei bulunamadı: {program}")
        return

    # Kullanıcıdan taranacak adresi alır.
    hedef = input("Hedef URL (http:// veya https://): ").strip()
    adres = urlsplit(hedef)

    if adres.scheme not in ("http", "https") or not adres.netloc:
        print("Geçerli bir http:// veya https:// adresi gir.")
        return

    try:
        sonuc = subprocess.run(
            [str(program), "-u", hedef],
            check=False,
        )

        if sonuc.returncode != 0:
            print(f"Nuclei hata koduyla tamamlandı: {sonuc.returncode}")

    except OSError as hata:
        print(f"Nuclei başlatılamadı: {hata}")


if __name__ == "__main__":
    nuclei_tara()