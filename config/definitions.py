"""Define global constants used in the project."""
import os
import tomllib
from typing import Any

ROOT_DIRECTORY: str = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
MAIN_PATH: str = os.path.join(ROOT_DIRECTORY, "main.py")
ASSETS_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "assets")
LOGS_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "logs")

with open(ROOT_DIRECTORY + "/pyproject.toml", "rb") as pyproject:
    PYPROJECT_DATA: dict[str, Any] = tomllib.load(pyproject)
