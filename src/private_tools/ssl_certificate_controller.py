import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse
def SSL_certificate():
    adres = input("Site adresi: ").strip()
    site = urlparse(adres if "://" in adres else "//" + adres).hostname

    try:
        if not site:
            raise ValueError("Geçerli bir site adresi gir.")

        context = ssl.create_default_context()
        with socket.create_connection((site, 443), timeout=5) as baglanti:
            with context.wrap_socket(baglanti, server_hostname=site) as tls:
                sertifika = tls.getpeercert()

        bitis = datetime.fromtimestamp(
            ssl.cert_time_to_seconds(sertifika["notAfter"]), timezone.utc
        )
        kalan = (bitis - datetime.now(timezone.utc)).days

        print(f"Site: {site}")
        print(f"Bitiş: {bitis:%d.%m.%Y}")
        print(f"Kalan: {kalan} gün")
        print("UYARI: Sertifika yakında bitiyor!" if kalan < 30 else "Süre uygun.")

    except (OSError, ValueError) as hata:
        print(f"Kontrol başarısız: {hata}")

if __name__ == "__main__":
    SSL_certificate()