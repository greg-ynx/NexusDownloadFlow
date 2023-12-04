"""
Test file is used to test NexusDownloadFlow's v1.0.0 algorithm.

The algorithm used is the grayscale template matching and the TM_SQDIFF comparison method from OpenCV.
"""

import os
import sys
import time
from typing import Any

import cv2
import pyautogui
from cv2.typing import MatLike
from mss import mss

from config.definitions import ASSETS_DIRECTORY

SCREENSHOT: str = "screenshot.png"
TEST_TEXT: str = "[TEST] [1.0.0] "
THRESHOLD: int = 3000


def _logging_test(text: str) -> None:
    sys.stdout.write(TEST_TEXT + text + "\n")


def _load_templates() -> list[MatLike]:
    return [
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template1.png")),
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template2.png")),
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template3.png")),
    ]


def _init_templates() -> list[MatLike]:
    return [cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) for template in _load_templates()]


def _test_algorithm() -> None:
    _logging_test("ndf-1.0.0-grayscale-template-matching.")
    _logging_test("Comparaison method: TM_SQDIFF.")
    try:
        with mss() as mss_instance:
            while True:
                monitors_size: dict[str, int] = mss_instance.monitors[0]
                monitors_left_top: tuple[Any, Any] = (monitors_size.get("left"), monitors_size.get("top"))
                screenshot: MatLike = cv2.imread(next(mss_instance.save(mon=-1, output=SCREENSHOT)))
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                for template in _init_templates():
                    match_template: MatLike = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF)
                    min_value, _, min_location, _ = cv2.minMaxLoc(match_template)
                    if min_value < THRESHOLD:
                        _logging_test("Match found!")
                        match_left_top_location: tuple[int, int] = (
                            min_location[0] + monitors_left_top[0],
                            min_location[1] + monitors_left_top[1],
                        )
                        template_height, template_width = template.shape
                        target: tuple[float, float] = (
                            match_left_top_location[0] + template_width / 2,
                            match_left_top_location[1] + template_height / 2,
                        )
                        pyautogui.moveTo(target)
                        time.sleep(6)
                        break
    except SystemExit:
        _logging_test("Exiting the program...")
        raise
    finally:
        if os.path.exists(SCREENSHOT):
            os.remove(SCREENSHOT)
        else:
            _logging_test("The file does not exist")
        _logging_test("Program ended")


if __name__ == "__main__":
    _test_algorithm()
