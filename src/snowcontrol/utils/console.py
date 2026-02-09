from rich.console import Console
from rich.theme import Theme

THEME = Theme(
    {
        "info": "cyan",
        "success": "green",
        "warning": "yellow",
        "error": "bold red",
    }
)

console = Console(theme=THEME)


def print_info(message: str) -> None:
    console.print(message, style="info")


def print_success(message: str) -> None:
    console.print(message, style="success")


def print_warning(message: str) -> None:
    console.print(message, style="warning")


def print_error(message: str) -> None:
    console.print(message, style="error")
