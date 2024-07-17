"""Issue file generator command module."""

import logging
import os.path
import platform

import psutil
import typer
from mss import mss

from config.application_properties import PROJECT_VERSION
from config.definitions import ISSUE_TEMPLATE_FILE_PATH
from config.ndf_logging import logging_report, setup_logging, stop_logging

__DEFAULT_ISSUE_FILE_NAME: str = ""
__DEFAULT_ISSUE_FILE_EXTENSION: str = ".txt"
__ISSUE_FILE_COMPLETE_NAME: str = __DEFAULT_ISSUE_FILE_NAME + __DEFAULT_ISSUE_FILE_EXTENSION

# Messages
__ISSUE_TITLE_PROMPT_MESSAGE: str = "Please enter a title for your issue"
__ISSUE_DESCRIPTION_PROMPT_MESSAGE: str = "Please describe your issue"
__ISSUE_FILE_PATH_IS_NOT_A_DIRECTORY_WARNING_MESSAGE: str = (
    "Given option --issue-folder-path is not a directory. Creating issue text file at the executable location."
)
__STARTING_MESSAGE: str = "Initiate the creation of an issue file..."
__SUCCESS_MESSAGE: str = "The issue file was successfully created."


def cli_issue(issue_folder_path: str | None = None) -> None:
    """Create the issue text file to copy/paste to our repository on GitHub."""
    setup_logging()
    logging.info(__STARTING_MESSAGE)
    try:
        output_file_path: str = __get_issue_file_path(issue_folder_path)

        issue_title: str = typer.prompt("Please enter a title for your issue")
        issue_description: str = typer.prompt("Please describe your issue")
        system_info: dict[str, str] = __get_user_system_info()
        ndf_version: str = PROJECT_VERSION

        filled_issue_content: str = __fill_issue_template(
            issue_title=issue_title, ndf_version=ndf_version, issue_description=issue_description, **system_info
        )

        __write_issue_file(output_file_path, filled_issue_content)
        print(filled_issue_content)
        logging.info(__SUCCESS_MESSAGE)
    except FileNotFoundError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)
        logging_report()
    finally:
        stop_logging()


def __get_user_system_info() -> dict[str, str]:
    """Gather and return system information needed for the issue report."""
    user_operating_system = f"{platform.system()} {platform.release()}"
    user_operating_system_architecture = platform.architecture()[0]
    user_system_ram_capacity = str(round(psutil.virtual_memory().total / (1024**3), 2))

    with mss() as mss_instance:
        monitors = mss_instance.monitors[1:]
        user_monitors_count = str(len(monitors))
        user_monitors_resolutions = " - ".join(
            [f'{monitor.get("width")}x{monitor.get("height")}' for monitor in monitors]
        )

    return {
        "user_operating_system": user_operating_system,
        "user_operating_system_architecture": user_operating_system_architecture,
        "user_system_ram_capacity": user_system_ram_capacity,
        "user_monitors_count": user_monitors_count,
        "user_monitors_resolutions": user_monitors_resolutions,
    }


def __get_issue_file_path(issue_folder_path: str | None = __ISSUE_FILE_COMPLETE_NAME) -> str:
    """Determine the output file path for the issue file."""
    if issue_folder_path is not None and os.path.isdir(issue_folder_path):
        return os.path.join(issue_folder_path, __ISSUE_FILE_COMPLETE_NAME)
    logging.warning(__ISSUE_FILE_PATH_IS_NOT_A_DIRECTORY_WARNING_MESSAGE)
    return __ISSUE_FILE_COMPLETE_NAME


def __get_issue_template_content() -> str:
    """Read and return the content of the issue template file."""
    with open(ISSUE_TEMPLATE_FILE_PATH, "r") as issue_template_content:
        return issue_template_content.read()


def __fill_issue_template(**kwargs: str) -> str:
    """Fill the issue template with provided details and return the filled content."""
    return __get_issue_template_content().format(**kwargs)


def __write_issue_file(output_file_path: str, issue_content: str) -> None:
    """Write the filled issue content to a file."""
    with open(output_file_path, "w") as issue_file:
        issue_file.write(issue_content)
