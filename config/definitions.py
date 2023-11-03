"""Define global constants used in the project."""
import os
import sys
import tomllib
from typing import Any

_TEMP_DIRECTORY: str
_EXE_DIRECTORY: str = os.path.realpath(os.path.join(sys.executable, ".."))
_DEV_DIRECTORY: str = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
MAIN_PATH: str
ASSETS_DIRECTORY: str
LOGS_DIRECTORY: str
PYPROJECT_DIRECTORY: str

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    _TEMP_DIRECTORY = os.path.join(sys._MEIPASS)
    MAIN_PATH = os.path.join(_TEMP_DIRECTORY, "main.py")
    ASSETS_DIRECTORY = os.path.join(_TEMP_DIRECTORY, "assets")
    LOGS_DIRECTORY = os.path.join(_EXE_DIRECTORY, "logs")
    PYPROJECT_DIRECTORY = os.path.join(_TEMP_DIRECTORY, "pyproject.toml")
else:
    MAIN_PATH = os.path.join(_DEV_DIRECTORY, "main.py")
    ASSETS_DIRECTORY = os.path.join(_DEV_DIRECTORY, "assets")
    LOGS_DIRECTORY = os.path.join(_DEV_DIRECTORY, "logs")
    PYPROJECT_DIRECTORY = os.path.join(_DEV_DIRECTORY, "pyproject.toml")


with open(PYPROJECT_DIRECTORY, "rb") as pyproject:
    PYPROJECT_DATA: dict[str, Any] = tomllib.load(pyproject)
