"""Logging configuration."""

import logging
import os
import sys
import time
from logging import Handler
from typing import Iterable

from config.definitions import GITHUB_ISSUE_VALUE, LOGS_DIRECTORY

__GITHUB_ISSUE_URL: str = GITHUB_ISSUE_VALUE + "?q=is%3Aissue+is%3Aopen"
__LOG_EXTENSION: str = ".log"
__NDF_STR: str = "ndf"
__LOGFILE_NAME: str = time.strftime("%Y_%m_%d_") + __NDF_STR + __LOG_EXTENSION


def delete_logfile() -> None:
    """Delete the log file."""
    logging.debug("Try to delete the current logfile...")
    logfile_path: str = get_logfile_path()
    __stop_logging()
    if os.path.exists(logfile_path):
        os.remove(path=logfile_path)
        logging.debug("Logfile deleted.")


def get_logfile_path() -> str:
    """
    Getter for the current log file path.

    :return: Log file path.
    """
    return __setup_logfile_path()


def logging_report() -> None:
    """Log report to open an issue on the project's repository."""
    logging.critical("Please report this exception to our repository on GitHub: " + __GITHUB_ISSUE_URL)


def setup_logging() -> None:
    """Set up logging configuration."""
    if not __logs_directory_exists():
        os.makedirs(LOGS_DIRECTORY)
    __handlers: Iterable[Handler] = [logging.FileHandler(__setup_logfile_path()), logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        level=logging.INFO,
        handlers=__handlers,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y - %H:%M:%S",
    )
    logging.debug("Logger setup completed.")


def __logs_directory_exists() -> bool:
    """
    Check if the logs directory exists.

    :return: Bool value indicating if the logs directory exists.
    """
    return os.path.exists(LOGS_DIRECTORY)


def __setup_logfile_path() -> str:
    """
    Set up log file.

    :return: String representing the log file path.
    """
    return os.path.join(LOGS_DIRECTORY, __LOGFILE_NAME)


def __stop_logging() -> None:
    """Shut down the logger."""
    logging.shutdown()
