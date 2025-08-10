# src/capital_gains_calculator/__main__.py
from .infrastructure.cli import main as cli_main
from .infrastructure.di_container import AppContainer


def main():
    """Entry point that initializes the container and the CLI application."""
    container = AppContainer()
    container.wire(modules=[cli_main])

    cli_main.app()


if __name__ == "__main__":
    main()
