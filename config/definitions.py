"""Define global constants used in the project."""
import os
import sys
import tomllib
from typing import Any

__TEMP_DIRECTORY: str
__EXE_DIRECTORY: str = os.path.realpath(os.path.join(sys.executable, ".."))
__DEV_DIRECTORY: str = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

# Paths constants definition
ROOT_DIRECTORY: str
MAIN_PATH: str
SCREENSHOT_PATH: str
ASSETS_DIRECTORY: str
CONFIG_DIRECTORY: str
LOGS_DIRECTORY: str
PYPROJECT_PATH: str

# Directory names definition
ASSETS_DIRECTORY_NAME: str = "assets"
ISSUE_TEMPLATE_DIRECTORY_NAME: str = "issue"
TEMPLATE_MATCHING_DIRECTORY_NAME: str = "template_matching"
CONFIG_DIRECTORY_NAME: str = "config"
LOGS_DIRECTORY_NAME: str = "logs"
CUSTOM_TEMPLATES_DIRECTORY_NAME: str = "custom_templates"

# File names definition
MAIN_FILE_NAME: str = "main.py"
SCREENSHOT_FILE_NAME: str = "screenshot.png"
PYPROJECT_FILE_NAME: str = "pyproject.toml"
ISSUE_TEMPLATE_FILE_NAME: str = "issue.template"


def __set_path(directory: str, name: str) -> str:
    """
    Join a directory to a folder/file.

    :param directory: The directory that matches to the wanted environment.
    :param name: Name of the folder/file.
    :return: The absolute path of the folder/file.
    """
    return os.path.join(directory, name)


if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    __TEMP_DIRECTORY = os.path.join(sys._MEIPASS)
    ROOT_DIRECTORY = __EXE_DIRECTORY
    MAIN_PATH = __set_path(__TEMP_DIRECTORY, MAIN_FILE_NAME)
    SCREENSHOT_PATH = __set_path(__TEMP_DIRECTORY, SCREENSHOT_FILE_NAME)
    ASSETS_DIRECTORY = __set_path(__TEMP_DIRECTORY, ASSETS_DIRECTORY_NAME)
    CONFIG_DIRECTORY = __set_path(__TEMP_DIRECTORY, CONFIG_DIRECTORY_NAME)
    PYPROJECT_PATH = __set_path(__TEMP_DIRECTORY, PYPROJECT_FILE_NAME)
else:
    ROOT_DIRECTORY = __DEV_DIRECTORY
    MAIN_PATH = __set_path(ROOT_DIRECTORY, MAIN_FILE_NAME)
    SCREENSHOT_PATH = __set_path(ROOT_DIRECTORY, SCREENSHOT_FILE_NAME)
    ASSETS_DIRECTORY = __set_path(ROOT_DIRECTORY, ASSETS_DIRECTORY_NAME)
    CONFIG_DIRECTORY = __set_path(ROOT_DIRECTORY, CONFIG_DIRECTORY_NAME)
    PYPROJECT_PATH = __set_path(ROOT_DIRECTORY, PYPROJECT_FILE_NAME)

LOGS_DIRECTORY = __set_path(ROOT_DIRECTORY, LOGS_DIRECTORY_NAME)
ISSUE_TEMPLATE_DIRECTORY_PATH: str = __set_path(ASSETS_DIRECTORY, ISSUE_TEMPLATE_DIRECTORY_NAME)
ISSUE_TEMPLATE_FILE_PATH: str = __set_path(ISSUE_TEMPLATE_DIRECTORY_PATH, ISSUE_TEMPLATE_FILE_NAME)
TEMPLATE_MATCHING_DIRECTORY_PATH: str = __set_path(ASSETS_DIRECTORY, TEMPLATE_MATCHING_DIRECTORY_NAME)
CUSTOM_TEMPLATES_DIRECTORY_PATH: str = __set_path(ROOT_DIRECTORY, CUSTOM_TEMPLATES_DIRECTORY_NAME)

with open(PYPROJECT_PATH, "rb") as pyproject:
    PYPROJECT_DATA: dict[str, Any] = tomllib.load(pyproject)
    PROJECT_DATA: dict[str, Any] = PYPROJECT_DATA.get("project")  # type: ignore
    GITHUB_DATA: dict[str, str] = PYPROJECT_DATA.get("github")  # type: ignore
    GITHUB_ISSUE_VALUE: str = GITHUB_DATA.get("issues")  # type: ignore
