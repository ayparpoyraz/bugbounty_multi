import requests

url = input("Site Adresi: ").strip()
if not url.startswith(("http://", "https://")):
    url = "https://" + url

basliklar = {
    "Content-Security-Policy": "İçerik kaynaklarını sınırlar",
    "Strict-Transport-Security": "HTTPS kullanımını zorunlu kılar",
    "X-Content-Type-Options": "İçerik türü tahminini engeller",
    "X-Frame-Options": "Iframe içinde gösterimi sınırlar",
    "Referrer-Policy": "Referans adresi paylaşımını kontrol eder",
    "Permissions-Policy": "Tarayıcı özelliklerine erişimi sınırlar",
}

try:
    with requests.get(url, timeout=10, stream=True) as cevap:
        print(f"\nAdres: {cevap.url} | HTTP: {cevap.status_code}\n")

        for baslik, aciklama in basliklar.items():
            deger = cevap.headers.get(baslik)
            print(f"{'[VAR]' if deger else '[YOK]'} {baslik}")
            print(f"   {deger or aciklama}\n")

except requests.RequestException as hata:
    print(f"Bağlantı hatası: {hata}")
