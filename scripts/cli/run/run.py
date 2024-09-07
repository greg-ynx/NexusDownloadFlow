"""Run command module."""

import logging
import os
from time import sleep
from typing import Sequence, cast

import keyboard
from cv2 import COLOR_BGR2GRAY, Canny, TM_CCOEFF_NORMED, cvtColor, imread, matchTemplate, minMaxLoc, resize
from cv2.typing import MatLike
from mss import mss
from pyautogui import FAILSAFE_POINTS, FailSafeException, Point, leftClick, moveTo, position

from _global.constants.messages import (
    CUSTOM_TEMPLATES_FOLDER_DOES_NOT_EXIST_WARNING_MESSAGE,
    CUSTOM_TEMPLATES_FOLDER_EMPTY_WARNING_MESSAGE,
)
from config.definitions import CUSTOM_TEMPLATES_DIRECTORY_PATH, SCREENSHOT_PATH, TEMPLATE_MATCHING_DIRECTORY_PATH
from config.ndf_logging import logging_report, setup_logging, stop_logging
from scripts.cli.run.run_mode_enum import RunModeEnum

__EDGE_MIN_VALUE: int = 50
__EDGE_MAX_VALUE: int = 200

__SCALES: list[float] = [
    1.0,
    0.95789474,
    0.91578947,
    0.87368421,
    0.83157895,
    0.78947368,
    0.74736842,
    0.70526316,
    0.66315789,
    0.62105263,
    0.57894737,
    0.53684211,
    0.49473684,
    0.45263158,
    0.41052632,
    0.36842105,
    0.32631579,
    0.28421053,
    0.24210526,
    0.2,
]

__DEFAULT_TEMPLATES: list[MatLike] = [
    imread(os.path.join(TEMPLATE_MATCHING_DIRECTORY_PATH, "template1.png")),
    imread(os.path.join(TEMPLATE_MATCHING_DIRECTORY_PATH, "template2.png")),
    imread(os.path.join(TEMPLATE_MATCHING_DIRECTORY_PATH, "template3.png")),
]

__THRESHOLD: float = 0.65

__RUN_STARTING_MESSAGE: str = "NexusDownloadFlow is starting..."
__RUNNING_MESSAGE: str = "NexusDownloadFlow is running in {mode} mode."
__PAUSE_NDF_MESSAGE: str = "NexusDownloadFlow is now paused..."
__RESUME_NDF_MESSAGE: str = "NexusDownloadFlow has resumed..."
__STOPPING_NDF_MESSAGE: str = "Stopping NexusDownloadFlow..."
__EXITING_INFO_MESSAGE: str = "Exiting the program..."
__FAILSAFE_ERROR_MESSAGE: str = "Fail-safe triggered from mouse moving to a corner of the screen."
__SCREENSHOT_DOES_NOT_EXIST_MESSAGE: str = "The screenshot does not exist."
__PROGRAM_ENDED_MESSAGE: str = "Program ended."

__CUSTOM_RUN_NO_CUSTOM_TEMPLATE_FOUND_ERROR_MESSAGE: str = (
    "No custom template found. Please add a custom template with the `add-template` command before trying again."
)

is_running: bool = False
is_paused: bool = False


def cli_run(mode: str) -> None:
    """
    Run the auto-downloader.

    :raises KeyboardInterrupt: Raised when the user interrupts the program.
    :raises FailSafeException: Raised when the mouse position is on one of the corners of the screen.
    Should not be raised (open an issue on GitHub if it happens).
    :raises ValueError: Should not be raised (open an issue on GitHub if it happens).
    :raises Exception: For currently unknown exceptions (open an issue on GitHub if it happens).
    """
    setup_logging()
    logging.info(__RUN_STARTING_MESSAGE)
    try:
        match mode:
            case RunModeEnum.CLASSIC:
                classic_run()
            case RunModeEnum.CUSTOM:
                custom_run()
            case RunModeEnum.HYBRID:
                hybrid_run()
            case _:
                hybrid_run()
    except KeyboardInterrupt:
        logging.info(__EXITING_INFO_MESSAGE)
    except FailSafeException:
        logging.error(__FAILSAFE_ERROR_MESSAGE)
    except ValueError as e:
        logging.error(e)
        logging_report()
    except Exception as e:
        logging.error(e)
        logging_report()
    finally:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
        else:
            logging.warning(__SCREENSHOT_DOES_NOT_EXIST_MESSAGE)
        logging.info(__PROGRAM_ENDED_MESSAGE)
        stop_logging()
        input("Press any key to exit...")


def classic_run() -> None:
    logging.info(__RUNNING_MESSAGE.format(mode=RunModeEnum.CLASSIC))
    launch_ndf(__DEFAULT_TEMPLATES)


def custom_run() -> None:
    logging.info(__RUNNING_MESSAGE.format(mode=RunModeEnum.CUSTOM))
    custom_templates: list[MatLike] = __get_custom_templates()
    if custom_templates:
        launch_ndf(custom_templates)
        return
    logging.error(__CUSTOM_RUN_NO_CUSTOM_TEMPLATE_FOUND_ERROR_MESSAGE)


def hybrid_run() -> None:
    logging.info(__RUNNING_MESSAGE.format(mode=RunModeEnum.HYBRID))
    hybrid_templates: list[MatLike] = __DEFAULT_TEMPLATES + __get_custom_templates()
    launch_ndf(hybrid_templates)


def launch_ndf(templates: list[MatLike]) -> None:
    """Launch the auto-downloader."""
    global is_running, is_paused
    is_running = True

    __init_hotkeys()

    edged_templates: list[MatLike] = __get_edged_templates(templates)
    with mss() as mss_instance:
        while is_running:
            __when_paused()
            monitors_size: dict[str, int] = mss_instance.monitors[0]
            monitors_left_top: tuple[int, int] = __if_monitors_left_top_present(monitors_size)
            screenshot: MatLike = imread(next(mss_instance.save(mon=-1, output=SCREENSHOT_PATH)))
            grayscale_screenshot: MatLike = cvtColor(screenshot, COLOR_BGR2GRAY)
            multiscale_match_template(edged_templates, grayscale_screenshot, monitors_left_top)


def multiscale_match_template(
    templates: list[MatLike], screenshot: MatLike, left_top_coordinates: tuple[int, int]
) -> None:
    """
    Apply multiscale template matching algorithm.

    :param templates: List of edged templates to match.
    :param screenshot: Screenshot where the search is running.
    :param left_top_coordinates: Left-top pixel of the system monitor(s).
    """
    for scale in __SCALES:
        resized_screenshot: MatLike = __resize_screenshot(screenshot, scale)
        edged_screenshot: MatLike = Canny(resized_screenshot, 50, 200)
        for template in templates:
            potential_match: tuple[float, Sequence[int]] = __get_potential_match(edged_screenshot, template)
            potential_match_value: float = potential_match[0]
            potential_match_location: Sequence[int] = potential_match[1]
            if __is_match_found(potential_match_value):
                logging.info("Match found!")
                match_location_x: int = potential_match_location[0]
                match_location_y: int = potential_match_location[1]
                match_left_top_location: tuple[int, int] = (
                    match_location_x + left_top_coordinates[0],
                    match_location_y + left_top_coordinates[1],
                )
                template_height: int = template.shape[0]
                template_width: int = template.shape[1]
                target: tuple[float, float] = (
                    match_left_top_location[0] + template_width / 2,
                    match_left_top_location[1] + template_height / 2,
                )
                __click_on_target(target)
                sleep(6)
                return


def pause_resume() -> None:
    """
    Pause or resume the auto download process.
    """
    global is_paused
    if is_paused:
        is_paused = False
        logging.info(__RESUME_NDF_MESSAGE)
    else:
        is_paused = True
        logging.info(__PAUSE_NDF_MESSAGE)


def stop() -> None:
    """
    Stop the auto download process.
    """
    global is_running, is_paused
    is_running = False
    is_paused = False
    logging.info(__STOPPING_NDF_MESSAGE)


def __init_hotkeys() -> None:
    """Initialize the hotkeys."""
    keyboard.add_hotkey("F3", pause_resume)
    keyboard.add_hotkey("F4", stop)


def __when_paused() -> None:
    global is_paused
    while is_paused:
        continue


def __resize_screenshot(screenshot: MatLike, scale: float) -> MatLike:
    """
    Resize the input screenshot.

    :param screenshot: Screenshot to resize.
    :param scale: The scale factor to resize the screenshot.
    :return: Resized screenshot.
    """
    new_width: int = int(screenshot.shape[1] * scale)
    new_height: int = int(screenshot.shape[0] * scale)
    return cast(MatLike, resize(screenshot, (new_width, new_height)))


def __get_potential_match(screenshot: MatLike, template: MatLike) -> tuple[float, Sequence[int]]:
    """
    Get the potential match value and its location.

    :param screenshot: Source for template matching.
    :param template: Template to match.
    :return: Tuple of potential match value and location.
    """
    matches: MatLike = matchTemplate(screenshot, template, TM_CCOEFF_NORMED)
    potential_match: tuple[float, float, Sequence[int], Sequence[int]] = minMaxLoc(matches)
    max_value: float = potential_match[1]
    max_location: Sequence[int] = potential_match[3]
    return max_value, max_location


def __if_monitors_left_top_present(monitors_size: dict[str, int]) -> tuple[int, int]:
    """
    Handle Optional of monitors_left_top (if_present like).

    :param monitors_size: Dictionary containing left and top properties of the system's monitor(s).
    :raises ValueError: If any of the value is none.
    :return: If present, tuple representing the left-top pixel's coordinates of the system's monitor(s).
    """
    value_error_message: str = "Monitors size '{key}' value is None"

    monitors_left: int | None = monitors_size.get("left")
    monitors_top: int | None = monitors_size.get("top")
    if monitors_left is None:
        raise ValueError(value_error_message.format(key="left"))
    if monitors_top is None:
        raise ValueError(value_error_message.format(key="top"))
    return monitors_left, monitors_top


def __is_match_found(match_value: float) -> bool:
    """
    Check if a match is found.

    :param match_value: Value of the match to check.
    :return: Bool value indicating whether a match is found or not.
    """
    return match_value > __THRESHOLD


def __click_on_target(target_location: tuple[float, float]) -> None:
    """
    Click on the target that has been identified and move the cursor to its previous location.

    :param target_location: Tuple of target coordinates.
    """
    original_position: Point | tuple[int, int] = position()
    if original_position not in FAILSAFE_POINTS:
        leftClick(target_location)
        moveTo(original_position)
    else:
        logging.warning(f"Risk of fail-safe trigger: Mouse position is on a fail-safe point -> { original_position }")
        logging.info("NexusDownloadFlow did not click on the target.")


def __get_custom_templates() -> list[MatLike]:
    if not os.path.exists(CUSTOM_TEMPLATES_DIRECTORY_PATH):
        logging.warning(CUSTOM_TEMPLATES_FOLDER_DOES_NOT_EXIST_WARNING_MESSAGE)
        return []
    templates: list[MatLike] = [
        imread(custom_template) for custom_template in os.listdir(CUSTOM_TEMPLATES_DIRECTORY_PATH)
    ]
    if not templates:
        logging.warning(CUSTOM_TEMPLATES_FOLDER_EMPTY_WARNING_MESSAGE)
        return []
    return templates


def __get_edged_templates(templates: list[MatLike]) -> list[MatLike]:
    """
    Return the list of edged templates.

    :return: List of edged templates.
    """
    return [Canny(cvtColor(template, COLOR_BGR2GRAY), __EDGE_MIN_VALUE, __EDGE_MAX_VALUE) for template in templates]
