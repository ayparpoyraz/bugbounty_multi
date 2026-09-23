from pathlib import Path
from urllib.parse import urlsplit
import shutil
import subprocess


def whatweb_tara():
    ruby = shutil.which("ruby")

    script = (
        Path.home()
        / "Downloads"
        / "WhatWeb-master (1)"
        / "WhatWeb-master"
        / "whatweb"
    )

    if ruby is None:
        print("Ruby bulunamadı. Terminali veya VS Code'u yeniden aç.")
        return

    if not script.is_file():
        print(f"WhatWeb dosyası bulunamadı: {script}")
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
            [ruby, str(script), hedef],
            cwd=str(script.parent),
            check=False,
        )

        if sonuc.returncode != 0:
            print(f"WhatWeb hata koduyla tamamlandı: {sonuc.returncode}")

    except OSError as hata:
        print(f"WhatWeb başlatılamadı: {hata}")


if __name__ == "__main__":
    whatweb_tara()