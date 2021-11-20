import threading
import numpy as np
import cv2

from mobot.brain.agent import Agent
from mobot.utils.image_grid import ImageGrid
from mobot.utils.rate import Rate

class BallFollower(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.camera.register_callback(self.camera_cb)
        self.chassis.enable()
        self.control_thread = threading.Thread(target=self.control_thread)
        self.image_grid = ImageGrid(self, size=(1,3))

        self.ball = None
        self.width = None

    def on_start(self):
        self.control_thread.start()

    def control_thread(self):
        rate = Rate(20)
        while self.ok():
            if self.ball is not None:
                center = self.width // 2
                x,y,r = self.ball
                target_r = 50

                lateral_error = center - x
                longitudinal_error = target_r - r

                self.logger.info(f"lateral_error: {lateral_error}, longitudinal_error: {longitudinal_error}")

                w = self.lateral_policy(lateral_error)
                v = self.longitudinal_policy(longitudinal_error)

                self.chassis.set_cmdvel(v=v, w=w)
            else:
                self.chassis.set_cmdvel(v=0.0, w=0.0)
            rate.sleep()

    def lateral_policy(self, lateral_error):
        if lateral_error > 100:
            w = 0.5
        elif lateral_error < -100:
            w = -0.5
        else:
            w = 0
        return w

    def longitudinal_policy(self, longitudinal_error):
        if longitudinal_error > 20:
            v = 0.06
        elif longitudinal_error < -20:
            v = -0.06
        else:
            v = 0
        return v

    def camera_cb(self, image, metadata):
        self.width = metadata.width
        self.image_grid.new_image(image, index=(0,0))

        marked_image, seg_image, self.ball = self.segment_ball(np.flip(image, axis=-1))
        self.image_grid.new_image(np.flip(seg_image, axis=-1), index=(0,1))
        self.image_grid.new_image(np.flip(marked_image, axis=-1), index=(0,2))

    def segment_ball(self, image):
        marked_image = image.copy()

        lower_yellow = np.array([14, 82, 160])
        upper_yellow = np.array([56, 255, 255])

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        seg_image = cv2.bitwise_and(image, image, mask=mask)

        gray_image = cv2.cvtColor(seg_image, cv2.COLOR_BGR2GRAY)

        ball = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT,\
                                   3, 1000,\
                                   minRadius = 20,\
                                   maxRadius = 150,\
                                   param1 = 50,\
                                   param2 = 30)

        if ball is not None:
            ball = np.round(ball.squeeze()).astype("int")
            x, y, r = ball
            cv2.circle(marked_image, (x, y), r, (0, 255, 0), 4)

        return marked_image, seg_image, ball

if __name__ == "__main__":
    ball_follower = BallFollower()
    ball_follower.start()
