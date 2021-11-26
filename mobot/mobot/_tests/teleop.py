# MIT License
#
# Copyright (c) 2021 Mobotx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import threading
import argparse

from mobot.brain.agent import Agent
from mobot.utils.terminal import get_key, CTRL_PLUS_C
# from mobot.utils.image_grid import ImageGrid
from mobot.utils.rate import Rate
from mobot.utils.joystick import Joystick

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Ui:
    def setupUi(self, main_window):
        main_window.setWindowTitle("Joystick")
        central_widget = QWidget()
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
        main_window.setCentralWidget(central_widget)
        self.joystick = Joystick()
        grid_layout.addWidget(self.joystick,0,0)

class TeleopAgent(Agent):
    def __init__(self, joystick=None):
        Agent.__init__(self)
        self.joystick = joystick
        self.chassis.enable()
        if self.joystick is None:
            self.control_thread = threading.Thread(target=self.keyboard_teleop_thread)
        else:
            self.control_thread = threading.Thread(target=self.joystick_teleop_thread)
            self.joystick.pose.connect(self.joystick_cb)
            self.v = 0.0
            self.w = 0.0

        # self.camera.register_callback(self.camera_cb)
        # self.image_grid = ImageGrid(self)

    def on_start(self):
        self.control_thread.start()

    # TODO: Implement mapping (x,y) --> (v,w)
    def joystick_cb(self, x, y):
        wmax = (self.chassis.wheel_diameter * self.chassis.max_wheel_speed)/self.chassis.wheel_to_wheel_separation
        vmax = (self.chassis.wheel_diameter * self.chassis.max_wheel_speed)/2
        self.v = -(y/100) * vmax
        self.w = -(x/100) * wmax
        # print(f"v: {v}, w: {w}")

    def joystick_teleop_thread(self):
        rate = Rate(30)
        while self.ok():
            self.chassis.set_cmdvel(v=self.v, w=self.w)
            rate.sleep()

    def keyboard_teleop_thread(self):
        self.bindings = {'w':( 0.07,  0.0),\
                         'a':( 0.0,  0.5),\
                         's':(-0.07,  0.0),\
                         'd':( 0.0, -0.5),\
                         ' ':( 0.0,  0.0)}
        self.help_msg = """
        Moving around:
                w
           a    s    d

        Spacebar to Stop!
        CTRL-C to quit
        """
        self.logger.info(self.help_msg)
        rate = Rate(30)
        while self.ok():
            key = get_key(0.1)
            if key == CTRL_PLUS_C:
                self.terminate()
                break
            if key in self.bindings:
                self.chassis.set_cmdvel(v=self.bindings[key][0], w=self.bindings[key][1])
            rate.sleep()

    # def camera_cb(self, image, metadata):
    #     self.image_grid.new_image(image)

def main():
    parser = argparse.ArgumentParser(description="Teleopration of Mobot")
    parser.add_argument('--joystick', action='store_true', help='Use joystick')
    args = parser.parse_args()

    if args.joystick:
        app = QApplication([])
        app.setStyle(QStyleFactory.create("Cleanlooks"))
        main_window = QMainWindow()
        ui = Ui()
        ui.setupUi(main_window)
        teleop_agent = TeleopAgent(joystick=ui.joystick)
        main_window.show()
        teleop_agent.start()
        if not app.exec():
            teleop_agent.terminate()
    else:
        teleop_agent = TeleopAgent()
        teleop_agent.start()

if __name__ == "__main__":
    main()
