"""Define global constants used in the project."""
import os
import sys
import tomllib
from typing import Any

__TEMP_DIRECTORY: str
__EXE_DIRECTORY: str = os.path.realpath(os.path.join(sys.executable, ".."))
__DEV_DIRECTORY: str = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
MAIN_PATH: str
SCREENSHOT_PATH: str
ASSETS_DIRECTORY: str
LOGS_DIRECTORY: str
PYPROJECT_PATH: str
MAIN_FILE_NAME: str = "main.py"
SCREENSHOT_FILE_NAME: str = "screenshot.png"
ASSETS_DIRECTORY_NAME: str = "assets"
LOGS_DIRECTORY_NAME: str = "logs"
PYPROJECT_FILE_NAME: str = "pyproject.toml"


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
    MAIN_PATH = __set_path(__TEMP_DIRECTORY, MAIN_FILE_NAME)
    SCREENSHOT_PATH = __set_path(__TEMP_DIRECTORY, SCREENSHOT_FILE_NAME)
    ASSETS_DIRECTORY = __set_path(__TEMP_DIRECTORY, ASSETS_DIRECTORY_NAME)
    LOGS_DIRECTORY = __set_path(__EXE_DIRECTORY, LOGS_DIRECTORY_NAME)
    PYPROJECT_PATH = __set_path(__TEMP_DIRECTORY, PYPROJECT_FILE_NAME)
else:
    MAIN_PATH = __set_path(__DEV_DIRECTORY, MAIN_FILE_NAME)
    SCREENSHOT_PATH = __set_path(__DEV_DIRECTORY, SCREENSHOT_FILE_NAME)
    ASSETS_DIRECTORY = __set_path(__DEV_DIRECTORY, ASSETS_DIRECTORY_NAME)
    LOGS_DIRECTORY = __set_path(__DEV_DIRECTORY, LOGS_DIRECTORY_NAME)
    PYPROJECT_PATH = __set_path(__DEV_DIRECTORY, PYPROJECT_FILE_NAME)


with open(PYPROJECT_PATH, "rb") as pyproject:
    PYPROJECT_DATA: dict[str, Any] = tomllib.load(pyproject)
    PROJECT_DATA: dict[str, Any] = PYPROJECT_DATA.get("project")
    GITHUB_DATA: dict[str, str] = PYPROJECT_DATA.get("github")
    GITHUB_ISSUE_VALUE: str = GITHUB_DATA.get("issues")
