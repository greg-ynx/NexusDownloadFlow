import os
import time

import pyautogui
import cv2
from mss import mss

from config.definitions import assets_dir

if __name__ == '__main__':
    print('NexusDownloadFlow 2022 starting...')
    print('Do not forget to replace the assets templates (1, 2 & 3) in order to match with the screenshots '
          'taken from your monitor!')
    try:
        templates = [cv2.imread(os.path.join(assets_dir, 'template1.png')),
                     cv2.imread(os.path.join(assets_dir, 'template2.png')),
                     cv2.imread(os.path.join(assets_dir, 'template3.png'))]
        with mss() as sct:
            while True:
                for i in range(1, 4):
                    template = templates[i - 1]
                    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                    screenshot = cv2.imread(sct.shot())
                    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                    res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_SQDIFF)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                    threshold = 3000
                    if min_val < threshold:
                        print('Matching template!')
                        top_left = min_loc
                        target = (top_left[0] + template_gray.shape[1] / 2, top_left[1] + template_gray.shape[0] / 2)
                        pyautogui.leftClick(target)
                        break
                time.sleep(6)
    except SystemExit:
        print('Exiting the program...')
        raise
    finally:
        time.sleep(5)
        if os.path.exists("monitor-1.png"):
            os.remove("monitor-1.png")
        else:
            print("The file does not exist")
        print('Program ended')
