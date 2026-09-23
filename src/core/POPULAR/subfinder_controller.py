from pathlib import Path
import re
import subprocess


def subfinder_tara():
    program = (
        Path.home()
        / "Downloads"
        / "Subfinder"
        / "subfinder.exe"
    )

    if not program.is_file():
        print(f"Subfinder bulunamadı: {program}")
        return

    domain = input("Alan adı (örnek: example.com): ").strip().rstrip(".")

    try:
        domain = domain.encode("idna").decode("ascii").lower()
    except UnicodeError:
        print("Geçersiz alan adı.")
        return

    etiketler = domain.split(".")
    gecerli = (
        len(domain) <= 253
        and len(etiketler) >= 2
        and all(
            re.fullmatch(
                r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?",
                etiket,
            )
            for etiket in etiketler
        )
    )

    if not gecerli:
        print("Yalnızca alan adı gir. Örnek: example.com")
        print("https:// veya /sayfa ekleme.")
        return

    print(f"Alt alan adları aranıyor: {domain}")

    try:
        sonuc = subprocess.run(
            [str(program), "-d", domain],
            check=False,
        )

        if sonuc.returncode != 0:
            print(f"Subfinder hata koduyla tamamlandı: {sonuc.returncode}")

    except OSError as hata:
        print(f"Subfinder başlatılamadı: {hata}")


if __name__ == "__main__":
    subfinder_tara()