"""Run file."""

import logging
import os
from time import sleep
from typing import Sequence, cast

from cv2 import COLOR_BGR2GRAY, TM_CCOEFF_NORMED, Canny, cvtColor, imread, matchTemplate, minMaxLoc, resize
from cv2.typing import MatLike
from mss import mss
from pyautogui import FAILSAFE_POINTS, FailSafeException, Point, leftClick, moveTo, position

from config.definitions import SCREENSHOT_PATH, TEMPLATE_MATCHING_DIRECTORY_PATH
from config.ndf_logging import delete_logfile, get_logfile_path, logging_report
from scripts.params import ask_to_keep_logfile

EDGE_MIN_VALUE: int = 50
EDGE_MAX_VALUE: int = 200
SCALES: list[float] = [
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
TEMPLATES: list[MatLike] = [
    imread(os.path.join(TEMPLATE_MATCHING_DIRECTORY_PATH, "template1.png")),
    imread(os.path.join(TEMPLATE_MATCHING_DIRECTORY_PATH, "template2.png")),
    imread(os.path.join(TEMPLATE_MATCHING_DIRECTORY_PATH, "template3.png")),
]
THRESHOLD: float = 0.65


def click_on_target(target_location: tuple[float, float]) -> None:
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


def get_potential_match(screenshot: MatLike, template: MatLike) -> tuple[float, Sequence[int]]:
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


def if_monitors_left_top_present(monitors_size: dict[str, int]) -> tuple[int, int]:
    """
    Handle Optional of monitors_left_top (if_present like).

    :param monitors_size: Dictionary containing left and top properties of the system's monitor(s).
    :raises ValueError: If any of the value is none.
    :return: If present, tuple representing the left-top pixel's coordinates of the system's monitor(s).
    """

    def error_message(_key: str) -> str:
        return f"Monitors' size '{_key}' value is None."

    monitors_left: int | None = monitors_size.get("left")
    monitors_top: int | None = monitors_size.get("top")
    if monitors_left is None:
        raise ValueError(error_message("left"))
    if monitors_top is None:
        raise ValueError(error_message("top"))
    return monitors_left, monitors_top


def init_templates() -> list[MatLike]:
    """
    Return the list of edged templates.

    :return: List of edged templates.
    """
    return [Canny(cvtColor(template, COLOR_BGR2GRAY), EDGE_MIN_VALUE, EDGE_MAX_VALUE) for template in TEMPLATES]


def is_match_found(match_value: float) -> bool:
    """
    Check if a match is found.

    :param match_value: Value of the match to check.
    :return: Bool value indicating whether a match is found or not.
    """
    return match_value > THRESHOLD


def resize_screenshot(screenshot: MatLike, scale: float) -> MatLike:
    """
    Resize the input screenshot.

    :param screenshot: Screenshot to resize.
    :param scale: The scale factor to resize the screenshot.
    :return: Resized screenshot.
    """
    new_width: int = int(screenshot.shape[1] * scale)
    new_height: int = int(screenshot.shape[0] * scale)
    return cast(MatLike, resize(screenshot, (new_width, new_height)))


def multiscale_match_template(
    templates: list[MatLike], screenshot: MatLike, left_top_coordinates: tuple[int, int]
) -> None:
    """
    Apply multiscale template matching algorithm.

    :param templates: List of edged templates to match.
    :param screenshot: Screenshot where the search is running.
    :param left_top_coordinates: Left-top pixel of the system monitor(s).
    """
    for scale in SCALES:
        resized_screenshot: MatLike = resize_screenshot(screenshot, scale)
        edged_screenshot: MatLike = Canny(resized_screenshot, 50, 200)
        for template in templates:
            potential_match: tuple[float, Sequence[int]] = get_potential_match(edged_screenshot, template)
            potential_match_value: float = potential_match[0]
            potential_match_location: Sequence[int] = potential_match[1]
            if is_match_found(potential_match_value):
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
                click_on_target(target)
                sleep(6)
                return


def run() -> None:
    """Run the auto-downloader."""
    logging.info("NexusDownloadFlow is running.")
    edged_templates: list[MatLike] = init_templates()
    with mss() as mss_instance:
        while True:
            monitors_size: dict[str, int] = mss_instance.monitors[0]
            monitors_left_top: tuple[int, int] = if_monitors_left_top_present(monitors_size)
            screenshot: MatLike = imread(next(mss_instance.save(mon=-1, output=SCREENSHOT_PATH)))
            grayscale_screenshot: MatLike = cvtColor(screenshot, COLOR_BGR2GRAY)
            multiscale_match_template(edged_templates, grayscale_screenshot, monitors_left_top)


def try_run() -> None:
    """
    Try to run the auto-downloader.

    :raises KeyboardInterrupt: Raised when the user interrupts the program.
    :raises FailSafeException: Raised when the mouse position is on one of the corners of the screen.
    Should not be raised (open an issue on GitHub if it happens).
    :raises ValueError: Should not be raised (open an issue on GitHub if it happens).
    :raises Exception: For currently unknown exceptions (open an issue on GitHub if it happens).
    """
    logging.info("NexusDownloadFlow is starting...")
    keep_logfile: bool = False
    try:
        keep_logfile = ask_to_keep_logfile()
        run()
    except KeyboardInterrupt:
        logging.info("Exiting the program...")
    except FailSafeException:
        logging.error("Fail-safe triggered from mouse moving to a corner of the screen.")
        keep_logfile = True
    except ValueError as e:
        logging.error(e)
        logging_report()
        keep_logfile = True
    except Exception as e:
        logging.error(e)
        logging_report()
        keep_logfile = True
    finally:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
        else:
            logging.warning("The screenshot does not exist.")
        logging.info("Program ended.")
        if keep_logfile:
            logging.info(f"Find logfile at: { get_logfile_path() }")
        else:
            delete_logfile()
        input("Press any key to exit...")
