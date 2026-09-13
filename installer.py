import platform
import subprocess
import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


console = Console()


BASE_DIR = Path(__file__).resolve().parent
TOOLS_CONFIG = BASE_DIR / "packet_requirements.json"


def run_command(command):
    try:
        subprocess.run(
            command,
            check=True
        )

    except subprocess.CalledProcessError:
        console.print(
            Panel(
                f"[bold red]Komut başarısız[/bold red]\n\n"
                f"[dim]{' '.join(command)}[/dim]",
                border_style="red",
                box=box.ROUNDED
            )
        )


def load_tools():
    try:
        with open(
            TOOLS_CONFIG,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        return data

    except FileNotFoundError:
        console.print(
            Panel(
                f"[bold red]JSON dosyası bulunamadı[/bold red]\n\n"
                f"[dim]{TOOLS_CONFIG}[/dim]",
                title="ERROR",
                border_style="red",
                box=box.ROUNDED
            )
        )

        return None

    except json.JSONDecodeError as error:
        console.print(
            Panel(
                f"[bold red]JSON formatı hatalı[/bold red]\n\n"
                f"[dim]{error}[/dim]",
                title="ERROR",
                border_style="red",
                box=box.ROUNDED
            )
        )

        return None


def get_tools(data):
    tools = []

    try:
        categories = data["tools"]

        table = Table(
            title="AVAILABLE TOOLS",
            box=box.ROUNDED,
            border_style="cyan",
            header_style="bold cyan"
        )

        table.add_column(
            "Category",
            style="bold blue"
        )

        table.add_column(
            "Tool",
            style="white"
        )

        for category, category_tools in categories.items():

            for tool in category_tools:

                table.add_row(
                    category.upper(),
                    tool
                )

                tools.append(tool)

        console.print(table)

    except (KeyError, TypeError):

        console.print(
            Panel(
                "[bold red]"
                "JSON içerisinde 'tools' yapısı bulunamadı."
                "[/bold red]",
                title="ERROR",
                border_style="red",
                box=box.ROUNDED
            )
        )

        return []

    return tools


def check_tools(package_manager, tools):
    available = []
    unavailable = []

    for tool in tools:

        if package_manager == "apt":

            result = subprocess.run(
                [
                    "apt-cache",
                    "show",
                    tool
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        elif package_manager == "dnf":

            result = subprocess.run(
                [
                    "dnf",
                    "info",
                    tool
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        elif package_manager == "pacman":

            result = subprocess.run(
                [
                    "pacman",
                    "-Si",
                    tool
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        else:
            unavailable.append(tool)
            continue

        if result.returncode == 0:
            available.append(tool)

        else:
            unavailable.append(tool)

    return available, unavailable


def install_tools(package_manager, tools):

    if not tools:

        console.print(
            Panel(
                "[yellow]Kurulacak araç bulunamadı.[/yellow]",
                border_style="yellow",
                box=box.ROUNDED
            )
        )

        return

    console.print()

    console.print(
        Panel(
            f"[bold cyan]Package Manager:[/bold cyan] "
            f"[bold white]{package_manager}[/bold white]\n"
            f"[bold cyan]Status:[/bold cyan] "
            f"[yellow]Paketler kontrol ediliyor...[/yellow]",
            title="INSTALLER",
            border_style="cyan",
            box=box.ROUNDED
        )
    )

    available, unavailable = check_tools(
        package_manager,
        tools
    )

    if unavailable:

        table = Table(
            title="UNAVAILABLE PACKAGES",
            box=box.ROUNDED,
            border_style="yellow",
            header_style="bold yellow"
        )

        table.add_column(
            "Tool",
            style="yellow"
        )

        table.add_column(
            "Status",
            style="red"
        )

        for tool in unavailable:

            table.add_row(
                tool,
                "Not found"
            )

        console.print(table)

    if not available:

        console.print(
            Panel(
                "[bold red]"
                "Kurulabilecek araç bulunamadı."
                "[/bold red]",
                border_style="red",
                box=box.ROUNDED
            )
        )

        return

    table = Table(
        title="INSTALLING",
        box=box.ROUNDED,
        border_style="green",
        header_style="bold green"
    )

    table.add_column(
        "Tool",
        style="white"
    )

    table.add_column(
        "Status",
        style="green"
    )

    for tool in available:

        table.add_row(
            tool,
            "Ready"
        )

    console.print(table)

    console.print()

    if package_manager == "apt":

        run_command([
            "sudo",
            "apt",
            "update"
        ])

        run_command([
            "sudo",
            "apt",
            "install",
            "-y",
            *available
        ])

    elif package_manager == "dnf":

        run_command([
            "sudo",
            "dnf",
            "install",
            "-y",
            *available
        ])

    elif package_manager == "pacman":

        run_command([
            "sudo",
            "pacman",
            "-S",
            "--needed",
            *available
        ])

    console.print()

    console.print(
        Panel(
            "[bold green]Installation process completed.[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
    )


def SYSTEM():

    console.print()

    console.print(
        Panel(
            "[bold cyan]BUG BOUNTY MULTI[/bold cyan]\n"
            "[dim]System & Security Tool Installer[/dim]",
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 2)
        )
    )

    console.print()

    os_name = platform.system()

    system_table = Table(
        title="SYSTEM INFORMATION",
        box=box.ROUNDED,
        border_style="blue",
        header_style="bold blue"
    )

    system_table.add_column(
        "Property",
        style="cyan"
    )

    system_table.add_column(
        "Value",
        style="white"
    )

    system_table.add_row(
        "Operating System",
        os_name
    )

    if os_name == "Windows":

        system_table.add_row(
            "Family",
            "Windows"
        )

        console.print(system_table)

        console.print(
            Panel(
                "[bold red]Windows desteklenmiyor.[/bold red]",
                border_style="red",
                box=box.ROUNDED
            )
        )

        return

    elif os_name == "Darwin":

        system_table.add_row(
            "Family",
            "macOS"
        )

        console.print(system_table)

        console.print(
            Panel(
                "[bold red]macOS desteklenmiyor.[/bold red]",
                border_style="red",
                box=box.ROUNDED
            )
        )

        return

    elif os_name == "Linux":

        system_table.add_row(
            "Family",
            "Linux"
        )

        try:

            with open(
                "/etc/os-release",
                "r",
                encoding="utf-8"
            ) as file:

                os_info = {}

                for line in file:

                    line = line.strip()

                    if (
                        not line
                        or "=" not in line
                    ):
                        continue

                    key, value = line.split(
                        "=",
                        1
                    )

                    os_info[key] = value.strip('"')

        except FileNotFoundError:

            console.print(system_table)

            console.print(
                Panel(
                    "[bold red]"
                    "/etc/os-release bulunamadı."
                    "[/bold red]",
                    border_style="red",
                    box=box.ROUNDED
                )
            )

            return

        distro = os_info.get(
            "ID",
            "unknown"
        )

        distro_like = os_info.get(
            "ID_LIKE",
            ""
        )

        system_table.add_row(
            "Distribution",
            distro
        )

        system_table.add_row(
            "Based On",
            distro_like or "N/A"
        )

        values = (
            f"{distro} {distro_like}"
        ).lower()

        # Packet Manager

        if any(x in values for x in [
            "debian",
            "ubuntu",
            "kali",
            "mint"
        ]):

            package_manager = "apt"

        elif any(x in values for x in [
            "fedora",
            "rhel",
            "centos",
            "rocky",
            "almalinux"
        ]):

            package_manager = "dnf"

        elif any(x in values for x in [
            "arch",
            "manjaro"
        ]):

            package_manager = "pacman"

        else:

            console.print(system_table)

            console.print(
                Panel(
                    "[bold red]"
                    "Desteklenmeyen Linux dağıtımı."
                    "[/bold red]",
                    border_style="red",
                    box=box.ROUNDED
                )
            )

            return

        system_table.add_row(
            "Package Manager",
            package_manager
        )

        console.print(system_table)

        data = load_tools()

        if data is None:
            return

        tools = get_tools(data)

        install_tools(
            package_manager,
            tools
        )

    else:

        console.print(
            Panel(
                "[bold red]"
                "Bilinmeyen işletim sistemi."
                "[/bold red]",
                border_style="red",
                box=box.ROUNDED
            )
        )


if __name__ == "__main__":
    SYSTEM()