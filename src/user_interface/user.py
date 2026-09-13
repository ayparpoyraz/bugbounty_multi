from rich.console import Console
from ..private_tools.http_secure_controller import http_secure
from ..private_tools.network_monitor_controller import network_monitor
from ..private_tools.slayer_documentry import sub_domain_scanner
from ..private_tools.ssl_certificate_controller import SSL_certificate

console = Console()

banner_out = r"""
██████╗ ██████╗ ████████╗ ██████╗  ██████╗  ██████╗ ██╗     
██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██╔═══██╗██║     
██████╔╝██████╔╝   ██║   ██║   ██║██║   ██║██║   ██║██║     
██╔══██╗██╔══██╗   ██║   ██║   ██║██║   ██║██║   ██║██║     
██████╔╝██████╔╝   ██║   ╚██████╔╝╚██████╔╝╚██████╔╝███████╗
╚═════╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝ 
"""


OPTIONS = """
[bold cyan]╭────────────────────────────────────────────╮
│                 MODULES                    │
╰────────────────────────────────────────────╯[/bold cyan]

  [bold cyan][01][/bold cyan]  HTTP Secure Controller
  [bold cyan][02][/bold cyan]  Network Monitor Controller
  [bold cyan][03][/bold cyan]  Subdomain Scanner
  [bold cyan][04][/bold cyan]  SSL Certificate Controller
  [bold cyan][05][/bold cyan]  Vulnerability Scanner
  [bold cyan][06][/bold cyan]  Crawler
  [bold cyan][09][/bold cyan]  Offensive Security
  [bold cyan][10][/bold cyan]  Online Attack

  [bold red][00][/bold red]  Exit

"""


def banner():
    
    console.print(f"[cyan]{banner_out}[/cyan]")
    console.print(OPTIONS)

banner()
secim = input('Select a module → ')

while True:
    if secim == '01':
        http_secure()
    elif secim == '02':
        network_monitor()
    elif secim == '03':
        sub_domain_scanner()
    elif secim == '04':
        SSL_certificate()
    





