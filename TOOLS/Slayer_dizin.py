import concurrent.futures
import requests
import sys
import time


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
}


def check_path(url, path):
    target_url = f"{url.rstrip('/')}/{path.lstrip('/')}"

    try:
        response = requests.get(
            target_url,
            headers=HEADERS,
            timeout=5,
            allow_redirects=False
        )

        status = response.status_code

        if status in [200, 204]:
            print(f"[+] Found: {target_url} (Status: {status})")

        elif status in [301, 302, 307, 308]:
            location = response.headers.get("Location", "Bilinmiyor")
            print(f"[*] Redirect: {target_url} -> {location} (Status: {status})")

        elif status == 403:
            print(f"[*] Forbidden: {target_url} (Status: 403)")

    except requests.RequestException:
        pass


def main():
    target_url = input("[?] Hedef URL: ").strip()
    wordlist_file = input("[?] Wordlist yolu: ").strip()

    if not target_url:
        print("[-] URL girilmedi.")
        return

    if not wordlist_file:
        print("[-] Wordlist yolu girilmedi.")
        return

    try:
        with open(
            wordlist_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:
            words = [line.strip() for line in f if line.strip()]

    except FileNotFoundError:
        print(f"[-] Hata: {wordlist_file} dosyası bulunamadı.")
        return

    print(f"\n[*] Hedef: {target_url}")
    print(f"[*] Yüklenen kelime sayısı: {len(words)}")
    print("[*] Taramaya başlanıyor...\n" + "+" * 40)

    start_time = time.time()

    threads = 15

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=threads
    ) as executor:

        futures = [
            executor.submit(check_path, target_url, word)
            for word in words
        ]

        concurrent.futures.wait(futures)

    elapsed_time = time.time() - start_time
    print("-" * 40)
    print(f"[*] Tarama tamamlandı.")
    print(f"[*] Geçen süre: {elapsed_time:.2f} saniye.")


if __name__ == "__main__":
    main()
