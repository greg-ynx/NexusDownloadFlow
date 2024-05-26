"""Main executable file of NexusDownloadFlow."""
import logging

from config.ascii_art import print_ascii_art
from config.ndf_logging import setup_logging
from scripts.ndf_run import try_run


def main() -> None:
    """NexusDownloadFlow main function."""

    setup_logging()
    print_ascii_art()
    logging.info("NexusDownloadFlow is starting...")
    try_run()


if __name__ == "__main__":
    main()
