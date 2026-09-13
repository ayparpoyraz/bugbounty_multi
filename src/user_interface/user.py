
from rich.console import Console

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

  [bold cyan][01][/bold cyan]  Network Scanner
  [bold cyan][02][/bold cyan]  Web Scanner
  [bold cyan][03][/bold cyan]  Subdomain Enumeration
  [bold cyan][04][/bold cyan]  Port Scanner
  [bold cyan][05][/bold cyan]  Vulnerability Scanner
  [bold cyan][06][/bold cyan]  Crawler
  [bold cyan][09][/bold cyan]  Offensive Security
  [bold cyan][10][/bold cyan]  Online Attack

  [bold red][00][/bold red]  Exit

[dim]Select a module →[/dim] """


def banner():
    
    console.print(f"[cyan]{banner_out}[/cyan]")
    console.print(OPTIONS)

    # -end- 


