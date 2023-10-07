"""Print NexusDownloadFlow ascii art."""
import sys
from typing import Any

from config.definitions import PYPROJECT_DATA

ASCII_COLOR: str = "\033[33m"
ASCII_TEXT: str = """
 _   _
| \\ | |
|  \\| | _____  ___   _ ___
| . ` |/ _ \\ \\/ / | | / __|
| |\\  |  __/>  <| |_| \\__ \\
\\_| \\_/\\___/_/\\_\\__,_|___/
______                    _                 _  ______ _
|  _  \\                  | |               | | |  ___| |
| | | |_____      ___ __ | | ___   __ _  __| | | |_  | | _____      __
| | | / _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` | |  _| | |/ _ \\ \\ /\\ / /
| |/ / (_) \\ V  V /| | | | | (_) | (_| | (_| | | |   | | (_) \\ V  V /
|___/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_| \\_|   |_|\\___/ \\_/\\_/\
"""

PROJECT_DATA: Any = PYPROJECT_DATA.get("project")
PROJECT_VERSION: str = "v{0}".format(str(PROJECT_DATA.get("version")))


def print_ascii_art() -> None:
    sys.stdout.write(ASCII_COLOR + ASCII_TEXT + PROJECT_VERSION + "\033[0m\n")
print_ascii_art()
