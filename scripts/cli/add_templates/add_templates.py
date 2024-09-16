"""Add templates command module."""

import imghdr
import logging
import os
import shutil
from typing import List

from _global.constants.messages import (
    CUSTOM_TEMPLATES_DIRECTORY_IS_NOT_A_DIRECTORY_ERROR_MESSAGE,
    FILE_PATH_INVALID_FILE_ERROR_MESSAGE,
    FILE_PATH_INVALID_IMAGE_ERROR_MESSAGE,
)
from config.definitions import CUSTOM_TEMPLATES_DIRECTORY_PATH
from config.ndf_logging import logging_report, setup_logging, stop_logging

# Messages
__PATHS_NO_PATH_PROVIDED_ERROR_MESSAGE: str = "No path provided."

__CLI_ADD_TEMPLATES_START_MESSAGE: str = "Initiate the addition of custom templates..."
__CLI_ADD_TEMPLATES_SUCCESS_MESSAGE: str = "The user's template has been successfully added to '{file_path}'."


def cli_add_templates(paths: List[str]) -> None:
    """
    Add custom templates.

    :param paths: Path list of the templates.
    """
    setup_logging()
    try:
        logging.info(__CLI_ADD_TEMPLATES_START_MESSAGE)
        __check_paths(paths)

        for path in paths:
            __verify_image(path)

        # Check if the directory exists, create it if not
        if not os.path.exists(CUSTOM_TEMPLATES_DIRECTORY_PATH):
            os.makedirs(CUSTOM_TEMPLATES_DIRECTORY_PATH)
        elif not os.path.isdir(CUSTOM_TEMPLATES_DIRECTORY_PATH):
            raise NotADirectoryError(CUSTOM_TEMPLATES_DIRECTORY_IS_NOT_A_DIRECTORY_ERROR_MESSAGE)

        for path in paths:
            file_path: str = shutil.copy(path, CUSTOM_TEMPLATES_DIRECTORY_PATH)
            logging.info(__CLI_ADD_TEMPLATES_SUCCESS_MESSAGE.format(file_path=file_path))

    except ValueError as e:
        logging.error(e)
    except NotADirectoryError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        logging_report()
    finally:
        stop_logging()


def __check_paths(paths: List[str]) -> None:
    """Check that at least one path is provided."""
    if not paths:
        raise ValueError(__PATHS_NO_PATH_PROVIDED_ERROR_MESSAGE)


def __verify_image(file_path: str) -> None:
    """Verify that input file path is a valid image."""
    if not os.path.isfile(file_path):
        raise ValueError(FILE_PATH_INVALID_FILE_ERROR_MESSAGE.format(file_path=file_path))

    if imghdr.what(file_path) is None:
        raise ValueError(FILE_PATH_INVALID_IMAGE_ERROR_MESSAGE.format(file_path=file_path))
