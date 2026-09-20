from pathlib import Path
import subprocess


def gobuster_tara():
    program = (
        Path.home()
        / "Downloads"
        / "gobuster_Windows_x86_64"
        / "gobuster.exe"
    )

    if not program.is_file():
        print(f"Gobuster bulunamadı: {program}")
        return

    hedef = input("Hedef URL (http:// veya https://): ").strip()
    wordlist = Path(
        input("Wordlist dosyasının tam yolu: ").strip().strip('"')
    )

    if not hedef.startswith(("http://", "https://")):
        print("URL http:// veya https:// ile başlamalı.")
        return

    if not wordlist.is_file():
        print("Wordlist dosyası bulunamadı.")
        return

    sonuc = subprocess.run(
        [str(program), "dir", "-u", hedef, "-w", str(wordlist)],
        check=False,
    )

    if sonuc.returncode != 0:
        print(f"Gobuster hata koduyla tamamlandı: {sonuc.returncode}")


if __name__ == "__main__":
    gobuster_tara()