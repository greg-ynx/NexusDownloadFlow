"""Print NexusDownloadFlow ascii art."""
import sys

from config.application_properties import PROJECT_VERSION

__ASCII_COLOR: str = "\033[33m"
__ASCII_TEXT: str = """
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

__PROJECT_VERSION: str = "v{0}".format(PROJECT_VERSION)


def print_ascii_art() -> None:
    """Print NexusDownloadFlow ascii art with the project version."""
    sys.stdout.write(__ASCII_COLOR + __ASCII_TEXT + __PROJECT_VERSION + "\033[0m\n")
