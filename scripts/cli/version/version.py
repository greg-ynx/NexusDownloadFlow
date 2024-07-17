"""Version command module."""

from config.application_properties import PROJECT_VERSION


def cli_version() -> None:
    """Print the current version of the program."""
    print(f"v{ PROJECT_VERSION }")
