"""Logging configuration."""

import logging
import os
import sys
import time
from logging import Handler
from typing import Iterable

from config.definitions import LOGS_DIRECTORY

_LOG_EXTENSION: str = ".log"
_NDF_STR: str = "ndf"
_LOGFILE_NAME: str = time.strftime("%Y_%m_%d_") + _NDF_STR + _LOG_EXTENSION


def _setup_logfile_path() -> str:
    """
    Set up logfile.

    :return: Logfile path.
    """
    return os.path.join(LOGS_DIRECTORY, _LOGFILE_NAME)


def _stop_logging() -> None:
    """
    Shut down the logger listener.

    :return: None.
    """
    logging.shutdown()


HANDLERS: Iterable[Handler] = [logging.FileHandler(_setup_logfile_path()), logging.StreamHandler(sys.stdout)]


def get_logfile_path() -> str:
    """
    Getter for the current logfile path.

    :return: Logfile path.
    """
    return _setup_logfile_path()


def setup_logging() -> None:
    """
    Set up logging configuration.

    :return: None.
    """
    logging.basicConfig(
        level=logging.INFO,
        handlers=HANDLERS,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y - %H:%M:%S",
    )
    logging.debug("Logger setup complete.")


def delete_logfile() -> None:
    """
    Delete the logfile.

    :return: None.
    """
    logging.debug("Try to delete the current logfile...")
    logfile_path: str = get_logfile_path()
    _stop_logging()
    if os.path.exists(logfile_path):
        os.remove(path=logfile_path)
        logging.debug("Logfile deleted.")


def logging_report() -> None:
    """
    Log report to open an issue on the project's repository.

    :return: None.
    """
    logging.critical(
        "Please report this exception to our repository on GitHub: "
        "https://github.com/greg-ynx/NexusDownloadFlow/issues?q=is%3Aissue+is%3Aopen"
    )
