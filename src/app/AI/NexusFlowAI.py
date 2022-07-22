import numpy as np
import cv2
from mss import mss
from PIL import Image

class NexusFlowAI:
    def __init__(self):
        self.screenshot = None
        self.template = cv2.imread('template_sample.png')
        self.min_val, self.max_val, self.min_loc, self.max_loc = cv2minMaxLoc(self.match())
        self.running = False
        with mss() as sct:
            while self.running:
                self.screenshot = sct.shot()
                img = Image.frombytes(
                    'RGB',
                    (self.screenshot.width, self.screenshot.height),
                    self.screenshot.rgb,
                )
    def match(self):
        return cv2.matchTemplate(self.screenshot, self.template, cv2.TM_SQDIFF)

