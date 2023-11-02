"""Main executable file of NexusDownloadFlow."""
import logging

from config.ascii_art import print_ascii_art
from config.ndf_logging import setup_logging
from scripts.ndf_params import ask_to_keep_logfile
from scripts.ndf_run import try_run


def main() -> None:
    """
    NexusDownloadFlow main function.

    :return: None.
    """
    setup_logging()
    print_ascii_art()
    logging.info("NexusDownloadFlow is starting...")
    keep_logfile: bool = ask_to_keep_logfile()
    try_run(keep_logfile)


if __name__ == "__main__":
    main()
