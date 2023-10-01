import os
import time
from typing import Sequence

import cv2
import pyautogui
from cv2.typing import MatLike
from mss import mss
from mss.base import MSSBase

from config.definitions import assets_dir


# TODO: use doc comments for every function
# TODO: add logs through the script and generate a log file based on the running day
# TODO: may add unit test

def init_templates() -> list[MatLike]:
    return [cv2.imread(os.path.join(assets_dir, 'template1.png')),
            cv2.imread(os.path.join(assets_dir, 'template2.png')),
            cv2.imread(os.path.join(assets_dir, 'template3.png'))]


def click_on_target(match_location: Sequence[int], template_shape: tuple[int, ...]) -> None:
    top_left_x: int
    top_left_y: int
    top_left_x, top_left_y = match_location
    target = (top_left_x + template_shape[1] / 2, top_left_y + template_shape[0] / 2)
    pyautogui.leftClick(target)


def search_template(mss_instance: MSSBase, threshold: float) -> None:
    template: MatLike
    for template in init_templates():
        template_gray: MatLike = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        screenshot: str = next(mss_instance.save(mon=-1, output='screenshot.png'))
        screenshot_gray: MatLike = cv2.cvtColor(cv2.imread(screenshot), cv2.COLOR_BGR2GRAY)
        match_template: MatLike = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_SQDIFF)
        min_value: float
        min_loc: Sequence[int]
        min_value, _, min_loc, _ = cv2.minMaxLoc(match_template)
        if min_value < threshold:
            print('Matching template!')
            click_on_target(min_loc, template_gray.shape)
            break


def main() -> None:
    print('NexusDownloadFlow is starting...')
    print('Do not forget to replace the assets templates (1, 2 & 3) in order to match with the screenshots '
          'taken from your monitor!')
    try:
        threshold: int = 3000
        with mss() as mss_instance:
            while True:
                search_template(mss_instance, threshold)
                time.sleep(6)
    except SystemExit:
        print('Exiting the program...')
        raise
    finally:
        if os.path.exists("screenshot.png"):
            os.remove("screenshot.png")
        else:
            print("The file does not exist")
        print('Program ended')


if __name__ == '__main__':
    main()
