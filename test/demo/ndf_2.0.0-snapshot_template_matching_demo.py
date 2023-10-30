"""
This test file is used to test NexusDownloadFlow's v2.0.0-SNAPSHOT algorithm.
The algorithm used is the edges template matching and the TM_CCOEFF_NORMED comparison method from OpenCV.
"""
import os
import time

import cv2
import pyautogui
from cv2.typing import MatLike
from mss import mss

from config.definitions import ASSETS_DIRECTORY


SCREENSHOT: str = "screenshot.png"
TEST_TEXT: str = "[TEST] [2.0.0-SNAPSHOT] "
THRESHOLD: float = .65


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


def test_algorithm() -> None:
    logging_test("ndf-2.0.0-snapshot-edges-template-matching.")
    logging_test("Comparaison method: TM_CCOEFF_NORMED.")
    try:
        with mss() as mss_instance:
            while True:
                monitors_size = mss_instance.monitors[0]
                monitors_left_top = (monitors_size.get("left"), monitors_size.get("top"))
                screenshot = cv2.imread(next(mss_instance.save(mon=-1, output=SCREENSHOT)))
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                screenshot = cv2.Canny(screenshot, 50, 200)
                for template in init_templates():
                    match_template = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                    _, max_value, _, max_location = cv2.minMaxLoc(match_template)
                    if max_value > THRESHOLD:
                        logging_test("Match found!")
                        match_left_top_location = (
                            max_location[0] + monitors_left_top[0],
                            max_location[1] + monitors_left_top[1],
                        )
                        template_height, template_width = template.shape
                        target = (
                            match_left_top_location[0] + template_width / 2,
                            match_left_top_location[1] + template_height / 2,
                        )
                        pyautogui.moveTo(target)
                        time.sleep(6)
                        break
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