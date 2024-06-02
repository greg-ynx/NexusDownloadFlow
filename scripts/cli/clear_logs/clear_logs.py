"""Clear logs command module."""

import logging
import os
import shutil

from config.definitions import LOGS_DIRECTORY
from config.ndf_logging import logging_report, setup_logging, stop_logging

# Messages
__STARTING_MESSAGE: str = "Initiate deletion of log folder files..."


def cli_clear_logs() -> None:
    """Clear the logs' folder."""
    print(__STARTING_MESSAGE)
    failed_count: int = 0
    if os.path.exists(LOGS_DIRECTORY):
        for item in os.listdir(LOGS_DIRECTORY):
            item_path: str = os.path.join(LOGS_DIRECTORY, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                setup_logging()
                logging.error(f"Error deleting {item_path}: {e}")
                logging_report()
        if failed_count == 0:
            print("The contents of the logs folder have been successfully deleted.")
        else:
            print(f"The contents of the logs folder have been partially deleted. {failed_count} items are remaining.")
    else:
        print("The logs folder do not exist.")
    stop_logging()
