import shutil
import subprocess


def nmap_tara():
    nmap_yolu = shutil.which("nmap")

    if nmap_yolu is None:
        print("Nmap bulunamadı. PATH ayarını kontrol et.")
        return

    hedef = input("Hedef IP veya alan adı: ").strip()

    if not hedef or hedef.startswith("-") or any(
        karakter.isspace() for karakter in hedef
    ):
        print("Tek bir IP veya alan adı gir.")
        return

    try:
        sonuc = subprocess.run([nmap_yolu, hedef], check=False)

        if sonuc.returncode != 0:
            print(f"Nmap hata koduyla tamamlandı: {sonuc.returncode}")
    except OSError as hata:
        print(f"Nmap başlatılamadı: {hata}")


if __name__ == "__main__":
    nmap_tara()