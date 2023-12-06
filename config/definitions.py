"""Define global constants used in the project."""
import os
import sys
import tomllib
from typing import Any

__TEMP_DIRECTORY: str
__EXE_DIRECTORY: str = os.path.realpath(os.path.join(sys.executable, ".."))
__DEV_DIRECTORY: str = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
MAIN_PATH: str
ASSETS_DIRECTORY: str
LOGS_DIRECTORY: str
PYPROJECT_DIRECTORY: str

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    __TEMP_DIRECTORY = os.path.join(sys._MEIPASS)
    MAIN_PATH = os.path.join(__TEMP_DIRECTORY, "main.py")
    ASSETS_DIRECTORY = os.path.join(__TEMP_DIRECTORY, "assets")
    LOGS_DIRECTORY = os.path.join(__EXE_DIRECTORY, "logs")
    PYPROJECT_DIRECTORY = os.path.join(__TEMP_DIRECTORY, "pyproject.toml")
else:
    MAIN_PATH = os.path.join(__DEV_DIRECTORY, "main.py")
    ASSETS_DIRECTORY = os.path.join(__DEV_DIRECTORY, "assets")
    LOGS_DIRECTORY = os.path.join(__DEV_DIRECTORY, "logs")
    PYPROJECT_DIRECTORY = os.path.join(__DEV_DIRECTORY, "pyproject.toml")


with open(PYPROJECT_DIRECTORY, "rb") as pyproject:
    PYPROJECT_DATA: dict[str, Any] = tomllib.load(pyproject)
    PROJECT_DATA: dict[str, Any] = PYPROJECT_DATA.get("project")
    GITHUB_DATA: dict[str, str] = PYPROJECT_DATA.get("github")
    GITHUB_ISSUE_VALUE: str = GITHUB_DATA.get("issues")
