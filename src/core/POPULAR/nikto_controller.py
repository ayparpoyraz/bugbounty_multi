import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

from rich.console import Console

console = Console()


def nikto_tara():
    nikto = shutil.which("nikto")

    if nikto:
        command = [nikto]
    else:
        perl = shutil.which("perl")
        if not perl:
            console.print("[red]Nikto veya Perl bulunamadı.[/red]")
            return

        script = Path(
            console.input("nikto.pl dosyasının yolu → ").strip().strip('"')
        ).expanduser()

        if not script.is_file():
            console.print("[red]nikto.pl dosyası bulunamadı.[/red]")
            return

        command = [perl, str(script.resolve())]

    target = console.input(
        "[cyan]Hedef URL (https://example.com) → [/cyan]"
    ).strip()

    parsed = urlsplit(target)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        console.print("[red]Geçerli bir HTTP/HTTPS adresi gir.[/red]")
        return

    result = subprocess.run(command + ["-h", target], check=False)

    if result.returncode != 0:
        console.print(
            f"[yellow]Nikto çıkış kodu: {result.returncode}[/yellow]"
        )

if __name__ == "__main__":
    nikto_tara()