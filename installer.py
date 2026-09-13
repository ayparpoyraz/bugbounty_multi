import os
import argparse


"""
[0] Sistem Bilgisi Al
[1] Sisteme Göre İndirmeler Yap
[END] Programı Başlat
"""

def SYSTEM():
    print(os.uname().nodename)





def main():
    parser = argparse.ArgumentParser(
        description="Requirements.txt yöneticisi"
    )


    # value__add_argument -> parser "-r"
    # value__add_argument -> parser "-i", "--install"
    parser.add_argument(
        "-r",
        required=True,
        help="Requirements.txt dosyasının yolu"
    )
    parser.add_argument(
        "-i",
        help="Kali Tools"
    )



    args = parser.parse_args()

    requirements_path = args.r

    if not os.path.isfile(requirements_path):
        print(f"[!] Dosya bulunamadı: {requirements_path}")
        return

    print(f"[+] Requirements bulundu: {requirements_path}")


    with open(
        requirements_path,
        "r",
        encoding="utf-8"
    ) as file:
        requirements = file.readlines()

    print("\n[+] Gereksinimler:")

    for requirement in requirements:
        requirement = requirement.strip()
        if not requirement or requirement.startswith("#"):
            continue
        print(f"    - {requirement}")


if __name__ == "__main__":
    main()