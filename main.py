import time
import numpy as np

import pyautogui
import cv2
from mss import mss


if __name__ == '__main__':
    print('NexusFlow 2022 starting...')
    screenshot = None
    template = cv2.imread('src/assets/template4_sample.png')
    template_w = template.shape[1]
    template_h = template.shape[0]
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    with mss() as sct:
        while True:
            screenshot = cv2.imread(sct.shot())
            sct_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(sct_gray, template_gray, cv2.TM_SQDIFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            threshold = 3000
            print("min " + str(min_val))
            print("max " + str(max_val))
            print("max-min " + str(max_val-min_val))
            if min_val < threshold:
                top_left = min_loc
                target = (top_left[0] + template_w/2, top_left[1] + template_h/2)
                pyautogui.leftClick(target)
            time.sleep(1)
    print('Program ended')

