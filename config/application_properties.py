"""Public application properties."""

from config.definitions import PROJECT_DATA

PROJECT_VERSION: str = str(PROJECT_DATA.get("version"))
