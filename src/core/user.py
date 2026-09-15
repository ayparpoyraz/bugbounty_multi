"""
___________________________________________________________________  
[!] Bu aracın amacı yeni başlayanlara güvenlik araçlarının
    ne işe yaradığını öğretmek ve araçları tek bir arayüz
    üzerinden çalıştırabilmektir.

[!] Kullanıcıdan kullanılacak araç seçilir, gerekli bilgiler alınır
    ve seçilen araç kendi işlem akışına göre çalıştırılır.

___________________________________________________________________    

[-TODO-]
:1 => WEB ile ilgili tüm araçları ekleyip çalıştırabilmek
:2 => Daha modern ve kullanıcı dostu arayüz
:3 => Optimize ve temiz proje yapısı

[-TAGS-]

[TAG]: WEB_SECURITY_TOOLS = #WST
[TAG]: CATEGORIES = #C10
[TAG]: private_tools = #pr_tools

<<<<<<< HEAD
[END]
EKLENENLER
1. nmap eklendi
2.gobuster eklendi
3.ffuf eklendi
4.nuclei eklendi
5.whatweb eklendi
6.wafw00f eklendi

YAPILACAKLAR
1. dosya yolları doğru girildi 
2. eklenen toolar optimize edilcek
3. yarı eklemeye devam etcem

"""



=======
___________________________________________________________________
"""
>>>>>>> origin/main
import os
from rich.console import Console
from rich.panel import Panel
<<<<<<< HEAD

from .private_tools.http_secure_controller import http_secure
from .private_tools.network_monitor_controller import network_monitor
from .private_tools.slayer_documentry import sub_domain_scanner
from .private_tools.ssl_certificate_controller import SSL_certificate
from .POPULAR.nmap_controller import nmap_tara
from .POPULAR.gosbuster_controller import gobuster_tara
from .POPULAR.ffuf_controller import ffuf_tara
from .POPULAR.Nuclei_controller import nuclei_tara
from .POPULAR.whatweb_controller import whatweb_tara
from .POPULAR.wafw00f_controller import wafw00f_tara
=======
# Private Tools -> 5
from private_tools.http_secure_controller import http_secure
from private_tools.network_monitor_controller import network_monitor
from private_tools.slayer_documentry import sub_domain_scanner
from private_tools.ssl_certificate_controller import SSL_certificate
from private_tools.http_login_brute_force import http_login_brute_force

>>>>>>> origin/main

damga = "[Private Tool]"

console = Console()


BANNER = r"""
██████╗ ██████╗ ████████╗ ██████╗  ██████╗  ██████╗ ██╗     
██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██╔═══██╗██║     
██████╔╝██████╔╝   ██║   ██║   ██║██║   ██║██║   ██║██║     
██╔══██╗██╔══██╗   ██║   ██║   ██║██║   ██║██║   ██║██║     
██████╔╝██████╔╝   ██║   ╚██████╔╝╚██████╔╝╚██████╔╝███████╗
╚═════╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝
"""


# Ana kategoriler
# Web Security aktif 14.09.2026

# C10
CATEGORIES = {
    "01": "Web Security", # ONLINE
    "02": "Network Security", # OFFLINE
    "03": "Reconnaissance", # OFFLINE
    "04": "Vulnerability Assessment", # OFFLINE
    "09": "Offensive Security", # OFFLINE
    "10": "Online Attack", # OFFLINE
}


# Web Security altında çalıştırılabilecek araçlar
# None = Araç henüz Python fonksiyonuna bağlanmadı

# WST
WEB_SECURITY_TOOLS = {
<<<<<<< HEAD
    "01": ("Nmap", nmap_tara), # ONLİNE
    "02": ("Gobuster", gobuster_tara),# ONLİNE
    "03": ("ffuf", ffuf_tara),# ONLİNE
    "04": ("Nikto", None),# OFFLINE
    "05": ("Nuclei",  nuclei_tara),# ONLİNE
    "06": ("WhatWeb", whatweb_tara),# ONLİNE
    "07": ("Wafw00f", wafw00f_tara),# ONLİNE
    "08": ("Amass", None),# OFFLINE
    "09": ("Subfinder", None),# OFFLINE
    "10": ("httpx", None),# OFFLINE
    "11": ("Feroxbuster", None),# OFFLINE
=======
    "01": ("Nmap", None), # OFFLINE
    "02": ("Gobuster", None), # OFFLINE
    "03": ("ffuf", None), # OFFLINE
    "04": ("Nikto", None), # OFFLINE
    "05": ("Nuclei", None), # OFFLINE
    "06": ("WhatWeb", None), # OFFLINE
    "07": ("Wafw00f", None), # OFFLINE
    "08": ("Amass", None), # OFFLINE
    "09": ("Subfinder", None), # OFFLINE
    "10": ("httpx", None), # OFFLINE
    "11": ("Feroxbuster", None), # OFFLINE

>>>>>>> origin/main
    # Kendi geliştirdiğimiz araçlar
    "12": ("HTTP Secure Controller", http_secure), # ONLINE
    "13": ("HTTP Login Brute Force", http_login_brute_force), # ONLINE
}


# Terminal ekranını temizler.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Menü başlığını gösterir.
def print_header(title):
    console.print(
        Panel(
            f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            expand=False
        )
    )


# Ana banner'ı gösterir.
def print_banner():
    console.print(f"[bold cyan]{BANNER}[/bold cyan]")


# HTTP Login Brute Force aracını çalıştırır.
def http_login_brute_force():

    clear_screen()
    print_banner()
    print_header("HTTP LOGIN BRUTE FORCE")

    target_url = console.input(
        "\n[bold cyan]Target URL → [/bold cyan]"
    ).strip()

    range_value = int(
        console.input(
            "[bold cyan]Password range → [/bold cyan]"
        ).strip()
    )

    zfill = int(
        console.input(
            "[bold cyan]Password digit count → [/bold cyan]"
        ).strip()
    )

    target_username = console.input(
        "[bold cyan]Target Username → [/bold cyan]"
    ).strip()

    username_parser = console.input(
        "[bold cyan]Username input parser → [/bold cyan]"
    ).strip()

    password_parser = console.input(
        "[bold cyan]Password input parser → [/bold cyan]"
    ).strip()

    wordlist = console.input(
        "[bold cyan]Wordlist path (optional) → [/bold cyan]"
    ).strip()

    login = Let(
        url=target_url,
        range_=range_value,
        zfill=zfill,
        username=target_username,
        username_parser=username_parser,
        passwd_parser=password_parser,
        wordlist=wordlist if wordlist else None
    )

    login.process()


# Ana kategori menüsünü gösterir.
def show_categories():
    clear_screen()
    print_banner()

    console.print(
        Panel(
            "\n".join([
                "[bold cyan][01][/bold cyan]  Web Security", # İlgili alanımız burası
                "[bold cyan][02][/bold cyan]  Network Security", # TODO
                "[bold cyan][03][/bold cyan]  Reconnaissance", # TODO
                "[bold cyan][04][/bold cyan]  Vulnerability Assessment", # TODO
                "[bold cyan][09][/bold cyan]  Offensive Security", # TODO
                "[bold cyan][10][/bold cyan]  Online Attack", # TODO
                "",
                "[bold red][00][/bold red]  Exit"
            ]),
            title="[bold white]CATEGORIES[/bold white]",
            border_style="cyan"
        )
    )


# Web Security
def web_security_menu():

    while True:

        clear_screen()
        print_banner()
        print_header("WEB SCANNERS")

        console.print(
            "\n".join([
                "[bold cyan][01][/bold cyan]  Nmap",
                "[bold cyan][02][/bold cyan]  Gobuster",
                "[bold cyan][03][/bold cyan]  ffuf",
                "[bold cyan][04][/bold cyan]  Nikto",
                "[bold cyan][05][/bold cyan]  Nuclei",
                "[bold cyan][06][/bold cyan]  WhatWeb",
                "[bold cyan][07][/bold cyan]  Wafw00f",
                "[bold cyan][08][/bold cyan]  Amass",
                "[bold cyan][09][/bold cyan]  Subfinder",
                "[bold cyan][10][/bold cyan]  httpx",
                "[bold cyan][11][/bold cyan]  Feroxbuster",

                # Kendi aracımızı diğer araçlardan ayırıyoruz
                f"[bold cyan][12][/bold cyan]  HTTP Secure Controller {damga}",
                f"[bold cyan][13][/bold cyan]  HTTP Login Brute Force {damga}",
                "[bold red][00][/bold red]  Back"
            ]),
        )

        selection = console.input(
            "\n[bold cyan]Select a tool => [/bold cyan]"
        ).strip()

        # Exit the menu
        if selection == "00":
            return

        # Girilen numaraya karşılık gelen aracı dictionary'den buluyoruz.
        tool = WEB_SECURITY_TOOLS.get(selection)

        # Dictionary'de böyle bir numara yoksa hata veriyoruz.
        if tool is None:
            console.print(
                "\n[bold red][!] Invalid selection.[/bold red]"
            )
            console.input(
                "\n[dim]Press Enter to continue...[/dim]"
            )
            continue

        # name = Araç adı
        # function = Araca bağlı Python fonksiyonu
        name, function = tool

        # Function None ise araç henüz kodumuza bağlanmamış demektir.
        if function is None:
            console.print(
                f"\n[yellow][!] {name} is not implemented yet.[/yellow]"
            )
            console.input(
                "\n[dim]Press Enter to continue...[/dim]"
            )
            continue

        clear_screen()
        print_banner()
        print_header(name)

        try:

            # Seçilen aracın Python fonksiyonunu çalıştırır.
            function()

        except KeyboardInterrupt:
            console.print(
                "\n[bold yellow][!] Tool interrupted.[/bold yellow]"
            )

        # Araç çalışırken başka bir hata oluşursa yakalanır.
        except ValueError:
            console.print(
                "\n[bold red][!] Invalid input. Please enter a valid value.[/bold red]"
            )

        except Exception as error:
            console.print(
                f"\n[bold red][!] Tool error:[/bold red] {error}"
            )
        console.input("\n[dim]Press Enter to return...[/dim]")


# Main function
def main():

    while True:
        show_categories()
        selection = console.input(
            "\n[bold cyan]Select a category → [/bold cyan]"
        ).strip()

        # Çıkış
        if selection == "00":
            clear_screen()
            console.print("[bold red]Exiting...[/bold red]")
            break






        # 01 -> Web Security 
        if selection == "01":
            web_security_menu()
            continue



        if selection not in CATEGORIES:
            console.print("\n[bold red][!] Invalid selection.[/bold red]")
            console.input("\n[dim]Press Enter to continue...[/dim]")
            continue

        clear_screen()
        print_banner()
        print_header(CATEGORIES[selection])

        console.print(
            f"\n[yellow][!] {CATEGORIES[selection]} "
            f"is not implemented yet.[/yellow]"
        )

        console.input(
            "\n[dim]Press Enter to return...[/dim]"
        )

if __name__ == "__main__":main()
