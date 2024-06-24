"""Messages constants module."""

from config.definitions import CUSTOM_TEMPLATES_DIRECTORY_PATH

NO_ACTION_REQUIRED_MESSAGE: str = "No action required."
CUSTOM_TEMPLATES_DIRECTORY_IS_NOT_A_DIRECTORY_ERROR_MESSAGE: str = (
    f"'{CUSTOM_TEMPLATES_DIRECTORY_PATH}' exists but is not a directory."
)
FILE_PATH_INVALID_FILE_ERROR_MESSAGE: str = "The provided path '{file_path}' is not a valid file."
FILE_PATH_INVALID_IMAGE_ERROR_MESSAGE: str = "The file '{file_path}' is not a valid image."
