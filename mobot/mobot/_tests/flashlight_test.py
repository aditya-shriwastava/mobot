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
from mobot.brain.agent import Agent

class MyAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.flashlight.enable()

        self.control_thread = threading.Thread(target=self.control_thread)

    def control_thread(self):
        self.logger.info("Waiting for flashlight to be available...")
        if self.flashlight.wait_until_available():
            self.logger.info("Flashlight available!")
            self.logger.info("Flashlight Turned On")
            self.flashlight.turn_on()

def main():
    my_agent = MyAgent()
    my_agent.start()
    my_agent.control_thread.start()

if __name__ == "__main__":
    main()
