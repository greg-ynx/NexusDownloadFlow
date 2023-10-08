"""Main executable file of NexusDownloadFlow."""
import os
import time
from typing import Optional, Sequence

import cv2
import pyautogui
from cv2.typing import MatLike
from mss import mss
from mss.base import MSSBase

from config.ascii_art import print_ascii_art
from config.definitions import ASSETS_DIRECTORY

# TODO: use doc comments for every function
# TODO: add logs through the script and generate a log file based on the running day
# TODO: may add unit test


SCREENSHOT: str = "screenshot.png"


def init_templates() -> list[MatLike]:
    """
    Return the list of templates.

    :return: list of templates
    """
    return [
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template1.png")),
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template2.png")),
        cv2.imread(os.path.join(ASSETS_DIRECTORY, "template3.png"))
    ]


def click_on_target(match_location: Sequence[int], template_shape: tuple[int, ...]) -> None:
    """
    Click on the target that has been identified and move the cursor to its previous location.

    :param Sequence[int] match_location: the coordinates of the pixels located at the top left of the matched image.
    :param tuple[int, ...] template_shape: the shape of the corresponding template
    """
    top_left_x: int
    top_left_y: int
    top_left_x, top_left_y = match_location
    original_position = pyautogui.position()
    target = (top_left_x + template_shape[1] / 2, top_left_y + template_shape[0] / 2)
    pyautogui.leftClick(target)
    pyautogui.moveTo(original_position)


def search_template(mss_instance: MSSBase, threshold: float) -> None:
    """
    Search and identify an image matching any templates with the specified threshold.

    :param MSSBase mss_instance: an instance of MSSBase
    :param float threshold: the threshold required to identify a match.
    """
    template: MatLike
    for template in init_templates():
        monitors_size: dict[str, int] = mss_instance.monitors[0]
        monitors_left_top: Sequence[Optional[int]] = (monitors_size.get('left'), monitors_size.get('top'))
        template_gray: MatLike = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        screenshot: str = next(mss_instance.save(mon=-1, output=SCREENSHOT))
        screenshot_gray: MatLike = cv2.cvtColor(cv2.imread(screenshot), cv2.COLOR_BGR2GRAY)
        match_template: MatLike = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_SQDIFF)
        min_value: float
        min_loc: Sequence[int]
        min_value, _, min_loc, _ = cv2.minMaxLoc(match_template)
        if monitors_left_top[0] is not None and monitors_left_top[1] is not None:
            min_loc = (min_loc[0] + monitors_left_top[0], min_loc[1] + monitors_left_top[1])
        if min_value < threshold:
            print("Matching template!")
            click_on_target(min_loc, template_gray.shape)
            time.sleep(6)
            break


def main() -> None:
    """
    NexusDownloadFlow main function.

    :raise SystemExit: raised when the window is closed
    """
    print_ascii_art()
    print("NexusDownloadFlow is starting...")
    print(
        "Do not forget to replace the assets templates (1, 2 & 3) in order to match with the screenshots "
        "taken from your monitor!"
    )
    try:
        threshold: int = 3000
        with mss() as mss_instance:
            while True:
                search_template(mss_instance, threshold)
    except SystemExit:
        print("Exiting the program...")
        raise
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
