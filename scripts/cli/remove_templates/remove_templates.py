"""Remove template command module."""

import logging
import ntpath
import os
import shutil
from typing import List

from _global.constants.messages import (
    CUSTOM_TEMPLATES_DIRECTORY_IS_NOT_A_DIRECTORY_ERROR_MESSAGE,
    CUSTOM_TEMPLATES_FOLDER_DOES_NOT_EXIST_WARNING_MESSAGE,
    FILE_PATH_INVALID_FILE_ERROR_MESSAGE,
    NO_ACTION_REQUIRED_MESSAGE,
)
from config.definitions import CUSTOM_TEMPLATES_DIRECTORY_PATH
from config.ndf_logging import logging_report, setup_logging, stop_logging

__PATHS_NO_PATH_GIVEN_WARNING_MESSAGE: str = f"No path given in input. {NO_ACTION_REQUIRED_MESSAGE}"
__DELETE_CUSTOM_TEMPLATES_FOLDER_START_MESSAGE: str = "Initiate custom_templates folder deletion..."
__DELETE_CUSTOM_TEMPLATES_FOLDER_SUCCESS_MESSAGE: str = "The custom templates folder has been successfully deleted!"
__GIVEN_PATH_NOT_IN_CUSTOM_TEMPLATES_DIRECTORY: str = (
    "File linked to given path '{path}' is not in custom_templates folder."
)
__DELETE_CUSTOM_TEMPLATE_FILE_START_MESSAGE: str = "Initiate '{filename}' file deletion..."
__DELETE_CUSTOM_TEMPLATE_FILE_SUCCESS_MESSAGE: str = (
    "The custom template file named '{filename}' has been successfully deleted!"
)


def cli_remove_templates(paths: List[str] | None, remove_all: bool = False) -> None:
    """Delete custom templates' directory."""
    setup_logging()
    try:
        if remove_all:
            __delete_custom_templates_folder()
            return
        if not os.path.exists(CUSTOM_TEMPLATES_DIRECTORY_PATH):
            logging.warning(CUSTOM_TEMPLATES_FOLDER_DOES_NOT_EXIST_WARNING_MESSAGE)
            return
        if paths:
            for path in paths:
                __delete_custom_template_file(path)
        else:
            logging.warning(__PATHS_NO_PATH_GIVEN_WARNING_MESSAGE)
    except NotADirectoryError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        logging_report()
    finally:
        stop_logging()


def __delete_custom_templates_folder() -> None:
    """Delete all custom template files."""
    logging.info(__DELETE_CUSTOM_TEMPLATES_FOLDER_START_MESSAGE)
    if os.path.exists(CUSTOM_TEMPLATES_DIRECTORY_PATH):
        if os.path.isdir(CUSTOM_TEMPLATES_DIRECTORY_PATH):
            shutil.rmtree(CUSTOM_TEMPLATES_DIRECTORY_PATH)
            logging.info(__DELETE_CUSTOM_TEMPLATES_FOLDER_SUCCESS_MESSAGE)
        else:
            raise NotADirectoryError(CUSTOM_TEMPLATES_DIRECTORY_IS_NOT_A_DIRECTORY_ERROR_MESSAGE)
    else:
        logging.warning(CUSTOM_TEMPLATES_FOLDER_DOES_NOT_EXIST_WARNING_MESSAGE)


def __delete_custom_template_file(path: str) -> None:
    """Delete one custom template file."""
    filename: str = ntpath.basename(path)
    logging.info(__DELETE_CUSTOM_TEMPLATE_FILE_START_MESSAGE.format(filename=filename))
    try:
        if os.path.isfile(path) or os.path.islink(path):
            if CUSTOM_TEMPLATES_DIRECTORY_PATH in path:
                os.unlink(path)
                logging.info(__DELETE_CUSTOM_TEMPLATE_FILE_SUCCESS_MESSAGE.format(filename=filename))
            else:
                raise ValueError(__GIVEN_PATH_NOT_IN_CUSTOM_TEMPLATES_DIRECTORY.format(path=path))
        else:
            raise ValueError(FILE_PATH_INVALID_FILE_ERROR_MESSAGE.format(file_path=path))
    except ValueError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        logging_report()
