"""Main executable file of NexusDownloadFlow."""

from config.ascii_art import print_ascii_art
from scripts.cli.commands import cli


def main() -> None:
    """NexusDownloadFlow main function."""
    print_ascii_art()
    cli()


if __name__ == "__main__":
    main()
