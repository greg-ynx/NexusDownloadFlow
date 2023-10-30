"""
This test file is used to test NexusDownloadFlow's v2.0.0 algorithm.
The algorithm used is the multiscale template matching and the TM_CCOEFF_NORMED comparison method from OpenCV.
"""
import os
import time
from typing import Any

import cv2
import pyautogui
from cv2.typing import MatLike
from mss import mss

from config.definitions import ASSETS_DIRECTORY

CHUNK_SLICES: list[float] = [
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
TEST_TEXT: str = "[TEST] [2.0.0] "
THRESHOLD: float = .65
SCREENSHOT: str = "screenshot.png"


def logging_test(text: str) -> None:
    print(TEST_TEXT + text)


def load_templates() -> list[MatLike]:
    return [
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template1.png")),
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template2.png")),
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template3.png")),
    ]


def init_templates() -> list[MatLike]:
    return [cv2.Canny(cv2.cvtColor(template, cv2.COLOR_BGR2GRAY), 50, 200) for template in load_templates()]


def multiscale_template_matching(screenshot: Any, left_top_coordinates: Any) -> None:
    for template in init_templates():
        for scale in CHUNK_SLICES:
            dsize_x, dsize_y = (int(screenshot.shape[1] * scale), int(screenshot.shape[0] * scale))
            resized_screenshot = cv2.resize(screenshot, (dsize_x, dsize_y))
            edges = cv2.Canny(resized_screenshot, 50, 200)
            match_template = cv2.matchTemplate(edges, template, cv2.TM_CCOEFF_NORMED)
            _, max_value, _, max_location = cv2.minMaxLoc(match_template)
            if max_value > THRESHOLD:
                logging_test("Match found!")
                match_left_top_location = (
                    max_location[0] + left_top_coordinates[0],
                    max_location[1] + left_top_coordinates[1],
                )
                template_height, template_width = template.shape
                target = (
                    match_left_top_location[0] + template_width / 2,
                    match_left_top_location[1] + template_height / 2,
                )
                pyautogui.moveTo(target)
                time.sleep(6)
                return


def test_algorithm() -> None:
    logging_test("ndf-2.0.0-multiscale-template-matching.")
    logging_test("Comparaison method: TM_CCOEFF_NORMED.")
    try:
        with mss() as mss_instance:
            while True:
                monitors_size = mss_instance.monitors[0]
                monitors_left_top = (monitors_size.get("left"), monitors_size.get("top"))
                screenshot = cv2.imread(next(mss_instance.save(mon=-1, output=SCREENSHOT)))
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                multiscale_template_matching(screenshot, monitors_left_top)
    except SystemExit:
        logging_test("Exiting the program...")
        raise
    finally:
        if os.path.exists(SCREENSHOT):
            os.remove(SCREENSHOT)
        else:
            logging_test("The file does not exist")
        logging_test("Program ended")


if __name__ == "__main__":
    test_algorithm()
