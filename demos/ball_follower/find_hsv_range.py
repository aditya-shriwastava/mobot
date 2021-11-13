import cv2
import numpy as np

from mobot.brain.agent import Agent
from mobot.utils.image_grid import ImageGrid

class FindHSV(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.camera.register_callback(self.camera_cb)
        self.image_grid = ImageGrid(self, size=(1,2))
        self.image_grid.create_trackbar("H Lower", 0, 255, on_change=self.h_lower_cb)
        self.image_grid.create_trackbar("S Lower", 0, 255, on_change=self.s_lower_cb)
        self.image_grid.create_trackbar("V Lower", 0, 255, on_change=self.v_lower_cb)
        self.image_grid.create_trackbar("H Upper", 255, 255, on_change=self.h_upper_cb)
        self.image_grid.create_trackbar("S Upper", 255, 255, on_change=self.s_upper_cb)
        self.image_grid.create_trackbar("V Upper", 255, 255, on_change=self.v_upper_cb)

        self.lower_hsv = np.array([0, 0, 0])
        self.upper_hsv = np.array([255, 255, 255])

    def apply_mask(self, image):
        image = np.flip(image, axis=-1) # From RGB to BGR
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_image, self.lower_hsv, self.upper_hsv)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        image = cv2.bitwise_and(image, image, mask=mask)
        return np.flip(image, axis=-1) # From BGR to RGB

    def camera_cb(self, image, metadata):
        self.image_grid.new_image(image, index=(0,0))
        self.image_grid.new_image(self.apply_mask(image), index=(0,1))

    def h_lower_cb(self, h):
        self.lower_hsv[0] = h

    def s_lower_cb(self, s):
        self.lower_hsv[1] = s

    def v_lower_cb(self, v):
        self.lower_hsv[2] = v

    def h_upper_cb(self, h):
        self.upper_hsv[0] = h
    
    def s_upper_cb(self, s):
        self.upper_hsv[1] = s

    def v_upper_cb(self, v):
        self.upper_hsv[2] = v

def main():
    find_hsv = FindHSV()
    find_hsv.start()

if __name__ == "__main__":
    main()


