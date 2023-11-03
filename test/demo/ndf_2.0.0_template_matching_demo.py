"""
Test file is used to test NexusDownloadFlow's v2.0.0 algorithm.

The algorithm used is the multiscale template matching and the TM_CCOEFF_NORMED comparison method from OpenCV.
"""
import os
import sys
from time import sleep
from typing import Sequence, cast

from cv2 import COLOR_BGR2GRAY, TM_CCOEFF_NORMED, Canny, cvtColor, imread, matchTemplate, minMaxLoc, resize
from cv2.typing import MatLike
from mss import mss
from pyautogui import moveTo

from config.definitions import ASSETS_DIRECTORY

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
TEST_TEXT: str = "[TEST] [2.0.0] "
THRESHOLD: float = 0.65


def _logging_test(text: str) -> None:
    sys.stdout.write(TEST_TEXT + text + "\n")


def _init_templates() -> list[MatLike]:
    return [Canny(cvtColor(template, COLOR_BGR2GRAY), EDGE_MIN_VALUE, EDGE_MAX_VALUE) for template in TEMPLATES]


def _resize_screenshot(screenshot: MatLike, scale: float) -> MatLike:
    new_width: int = int(screenshot.shape[1] * scale)
    new_height: int = int(screenshot.shape[0] * scale)
    return cast(MatLike, resize(screenshot, (new_width, new_height)))


def _get_potential_match(screenshot: MatLike, template: MatLike) -> tuple[float, Sequence[int]]:
    matches: MatLike = matchTemplate(screenshot, template, TM_CCOEFF_NORMED)
    potential_match: tuple[float, float, Sequence[int], Sequence[int]] = minMaxLoc(matches)
    max_value: float = potential_match[1]
    max_location: Sequence[int] = potential_match[3]
    return max_value, max_location


def _if_monitors_left_top_present(monitors_size: dict[str, int]) -> tuple[int, int]:
    monitors_left: int | None = monitors_size.get("left")
    monitors_top: int | None = monitors_size.get("top")
    if monitors_left is None:
        raise ValueError("monitors_size 'left' value is None")
    if monitors_top is None:
        raise ValueError("monitors_size 'top' value is None")
    return monitors_left, monitors_top


def _is_match_found(match_value: float) -> bool:
    return match_value > THRESHOLD


def _multiscale_match_template(
    templates: list[MatLike], screenshot: MatLike, left_top_coordinates: tuple[int, int]
) -> None:
    for scale in SCALES:
        resized_screenshot: MatLike = _resize_screenshot(screenshot, scale)
        edged_screenshot: MatLike = Canny(resized_screenshot, 50, 200)
        for template in templates:
            potential_match: tuple[float, Sequence[int]] = _get_potential_match(edged_screenshot, template)
            potential_match_value: float = potential_match[0]
            potential_match_location: Sequence[int] = potential_match[1]
            if _is_match_found(potential_match_value):
                _logging_test("Match found!")
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
                moveTo(target)
                sleep(6)
                return


def _test_algorithm() -> None:
    _logging_test("ndf-2.0.0-multiscale-template-matching.")
    _logging_test("Comparaison method: TM_CCOEFF_NORMED.")
    edged_templates: list[MatLike] = _init_templates()
    try:
        with mss() as mss_instance:
            while True:
                monitors_size: dict[str, int] = mss_instance.monitors[0]
                monitors_left_top: tuple[int, int] = _if_monitors_left_top_present(monitors_size)
                screenshot: MatLike = imread(next(mss_instance.save(mon=-1, output=SCREENSHOT)))
                grayscale_screenshot: MatLike = cvtColor(screenshot, COLOR_BGR2GRAY)
                _multiscale_match_template(edged_templates, grayscale_screenshot, monitors_left_top)
    except (SystemExit, KeyboardInterrupt):
        _logging_test("Exiting the program...")
        sys.exit(0)
    finally:
        if os.path.exists(SCREENSHOT):
            os.remove(SCREENSHOT)
        else:
            _logging_test("The file does not exist")
        _logging_test("Program ended")


if __name__ == "__main__":
    _test_algorithm()
