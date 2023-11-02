"""Main executable file of NexusDownloadFlow."""
import os
import sys
from time import sleep
from typing import Sequence, cast

from cv2 import COLOR_BGR2GRAY, TM_CCOEFF_NORMED, Canny, cvtColor, imread, matchTemplate, minMaxLoc, resize
from cv2.typing import MatLike
from mss import mss
from pyautogui import Point, leftClick, moveTo, position

from config.ascii_art import print_ascii_art
from config.definitions import ASSETS_DIRECTORY

# TODO: add logs through the script and generate a log file based on the running day
# TODO: may add unit test


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
SCREENSHOT: str = "screenshot.png"
TEMPLATES: list[MatLike] = [
    imread(os.path.join(ASSETS_DIRECTORY, "template1.png")),
    imread(os.path.join(ASSETS_DIRECTORY, "template2.png")),
    imread(os.path.join(ASSETS_DIRECTORY, "template3.png")),
]
THRESHOLD: float = 0.65


def init_templates() -> list[MatLike]:
    """
    Return the list of edged templates.

    :return: List of edged templates
    """
    return [Canny(cvtColor(template, COLOR_BGR2GRAY), EDGE_MIN_VALUE, EDGE_MAX_VALUE) for template in TEMPLATES]


def resize_screenshot(screenshot: MatLike, scale: float) -> MatLike:
    """
    Resize the input screenshot.

    :param screenshot: Screenshot to resize
    :param scale: Factor to resize the screenshot
    :return: resized screenshot.
    """
    new_width: int = int(screenshot.shape[1] * scale)
    new_height: int = int(screenshot.shape[0] * scale)
    return cast(MatLike, resize(screenshot, (new_width, new_height)))


def get_potential_match(screenshot: MatLike, template: MatLike) -> tuple[float, Sequence[int]]:
    """
    Get the potential match value and its location.

    :param screenshot: Source for template matching
    :param template: template to match
    :return: potential match value and location.
    """
    matches: MatLike = matchTemplate(screenshot, template, TM_CCOEFF_NORMED)
    potential_match: tuple[float, float, Sequence[int], Sequence[int]] = minMaxLoc(matches)
    max_value: float = potential_match[1]
    max_location: Sequence[int] = potential_match[3]
    return max_value, max_location


def if_monitors_left_top_present(monitors_size: dict[str, int]) -> tuple[int, int]:
    """
    Handle Optional of monitors_left_top (if_present like).

    :param monitors_size: Dictionary containing left and top properties of the system's monitor(s)
    :return: if present, the left-top pixel's coordinates of the system's monitor(s).
    """
    monitors_left: int | None = monitors_size.get("left")
    monitors_top: int | None = monitors_size.get("top")
    if monitors_left is None:
        raise ValueError("monitors_size 'left' value is None")
    if monitors_top is None:
        raise ValueError("monitors_size 'top' value is None")
    return monitors_left, monitors_top


def is_match_found(match_value: float) -> bool:
    """
    Check if a match is found.

    :param match_value: Value of the match to check
    :return: Whether the match is found or not.
    """
    return match_value > THRESHOLD


def multiscale_match_template(
    templates: list[MatLike], screenshot: MatLike, left_top_coordinates: tuple[int, int]
) -> None:
    """
    Apply multiscale template matching algorithm.

    :param templates: List of edged templates to match
    :param screenshot: screenshot where the search is running
    :param left_top_coordinates: left-top pixel of the system monitor(s)
    :return:
    """
    for scale in SCALES:
        resized_screenshot: MatLike = resize_screenshot(screenshot, scale)
        edged_screenshot: MatLike = Canny(resized_screenshot, 50, 200)
        for template in templates:
            potential_match: tuple[float, Sequence[int]] = get_potential_match(edged_screenshot, template)
            potential_match_value: float = potential_match[0]
            potential_match_location: Sequence[int] = potential_match[1]
            if is_match_found(potential_match_value):
                print("Match found!")
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


def click_on_target(target_location: tuple[float, float]) -> None:
    """
    Click on the target that has been identified and move the cursor to its previous location.

    :param target_location: Target coordinates
    """
    original_position: Point | tuple[int, int] = position()
    leftClick(target_location)
    moveTo(original_position)


def main() -> None:
    """
    NexusDownloadFlow main function.

    :raises SystemExit: raised when closing program
    :raises KeyboardInterrupt: raised when the user interrupts the program
    """
    print_ascii_art()
    print("NexusDownloadFlow is starting...")
    edged_templates: list[MatLike] = init_templates()
    try:
        with mss() as mss_instance:
            print("NexusDownloadFlow is running")
            while True:
                monitors_size: dict[str, int] = mss_instance.monitors[0]
                monitors_left_top: tuple[int, int] = if_monitors_left_top_present(monitors_size)
                screenshot: MatLike = imread(next(mss_instance.save(mon=-1, output=SCREENSHOT)))
                grayscale_screenshot: MatLike = cvtColor(screenshot, COLOR_BGR2GRAY)
                multiscale_match_template(edged_templates, grayscale_screenshot, monitors_left_top)
    except (SystemExit, KeyboardInterrupt):
        print("Exiting the program...")
        sys.exit(0)
    # except FailSafeException:
    #     # log error
    #     raise
    finally:
        if os.path.exists(SCREENSHOT):
            os.remove(SCREENSHOT)
        else:
            print("The file does not exist")
        print("Program ended")


if __name__ == "__main__":
    main()
