"""
[!] Bu aracın amacı yeni başlayanlar ve araçların ne gibi yerlerde kullanıldığını öğretir 

[!] Kullanıcya hangi aracı kullanmasını istediğini sorup 
    işlemlere devam etmek ve gerekli bilgileri alıp yapıcağınız 
    işlem türüne göre işleyişin devam etmesi

[-TODO-]
:1 => WEB ile ilgili tüm araçları ekleyip çalıştırabilmek
:2 => daha modern arayüz kulllanıcı dostu 
:3 => Optimize Temiz Proje Yapısı


[-TAGS-]

[TAG] WEB_SECURITY_TOOLS = #WST 
[TAG] CATEGORIES = #C10

[END]
"""


import os

from rich.console import Console
from rich.panel import Panel

from private_tools.http_secure_controller import http_secure
from private_tools.network_monitor_controller import network_monitor
from private_tools.slayer_documentry import sub_domain_scanner
from private_tools.ssl_certificate_controller import SSL_certificate


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

#C10
CATEGORIES = {
    "01": "Web Security", #ONLINE
    "02": "Network Security", #OFFLINE
    "03": "Reconnaissance", # OFFLINE
    "04": "Vulnerability Assessment", # OFFLINE
    "09": "Offensive Security", # OFFLINE
    "10": "Online Attack", # OFFLINE
}


# Web Security altında çalıştırılabilecek araçlar
# None = araç henüz Python fonksiyonuna bağlanmadı

#WST
WEB_SECURITY_TOOLS = {
    "01": ("Nmap", None), # OFFLINE
    "02": ("Gobuster", None),# OFFLINE
    "03": ("ffuf", None),# OFFLINE
    "04": ("Nikto", None),# OFFLINE
    "05": ("Nuclei", None),# OFFLINE
    "06": ("WhatWeb", None),# OFFLINE
    "07": ("Wafw00f", None),# OFFLINE
    "08": ("Amass", None),# OFFLINE
    "09": ("Subfinder", None),# OFFLINE
    "10": ("httpx", None),# OFFLINE
    "11": ("Feroxbuster", None),# OFFLINE
    # Kendi geliştirdiğimiz araçlar
    "12": ("HTTP Secure Controller", http_secure), #ONLINE
}


# Terminal ekranını temizler.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Menülerin üst kısmındaki başlığı oluşturur.
def print_header(title):
    console.print(
        Panel(
            f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            expand=False
        )
    )


# ASCII EKRANA BASTIR
def print_banner():
    console.print(f"[bold cyan]{BANNER}[/bold cyan]")


# Ana kategori menüsünü gösterir.
def show_categories():
    clear_screen()
    print_banner()

    console.print(
        Panel(
            "\n".join([
                "[bold cyan][01][/bold cyan]  Web Security", # İlgili Alanımız Burası
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

                # Kendi aracımızı diğer araçlardan ayırıyoruz.
                f"[bold cyan][12][/bold cyan]  HTTP Secure Controller {damga}",

                "",
                "[bold red][00][/bold red]  Back"
            ]),
        )

        # Kullanıcının seçimini alıyoruz.
        selection = console.input(
            "\n[bold cyan]Select a tool => [/bold cyan]"
        ).strip()

        # exit the menu
        if selection == "00":
            return

        # Girilen numaraya karşılık gelen aracı dictionary'den buluyoruz yani   "12": ("HTTP Secure Controller", http_secure),
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

            
        # name  = "Nmap"
        # function = None
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

        # CTRL+C ile araç durdurulursa program tamamen kapanmaz.
        except KeyboardInterrupt:
            console.print(
                "\n[bold yellow][!] Tool interrupted.[/bold yellow]"
            )

        # Araç çalışırken başka bir hata oluşursa yakalanır.
        except Exception as error:
            console.print(
                f"\n[bold red][!] Tool error:[/bold red] {error}"
            )

        # Araç bittikten sonra menüye dönmeden önce bekler.
        console.input(
            "\n[dim]Press Enter to return...[/dim]"
        )


# main func
def main():

    while True:
        
        show_categories() # Kategorileri

        # Kullanıcının kategori seçimini alır.
        selection = console.input(
            "\n[bold cyan]Select a category → [/bold cyan]"
        ).strip()

        #Çıkış
        if selection == "00":
            clear_screen()
            console.print(
                "[bold red]Exiting...[/bold red]"
            )
            break

        # 01--Web Security menüsüne girilir.
        if selection == "01":
            web_security_menu()
            continue

        # Henüz oluşturmadığımız kategoriler için uyarı.
        if selection not in CATEGORIES:
            console.print(
                "\n[bold red][!] Invalid selection.[/bold red]"
            )
            console.input(
                "\n[dim]Press Enter to continue...[/dim]"
            )
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



if __name__ == "__main__":
    main()

