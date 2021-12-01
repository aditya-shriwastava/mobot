import threading, time
import sys
import serial
from PyQt5 import QtCore, QtGui, QtWidgets

from ui_pid_tune import Ui_pid_tune
from mobot.utils.rate import Rate

class PIDTune(Ui_pid_tune):
    def __init__(self):
        super().__init__()
        self.mobot = serial.Serial(port='/dev/ttyUSB0',\
                                   baudrate=115200,\
                                   timeout=1)
        self.init_thread = threading.Thread(target=self.init_thread)
        self.w_present_thread = threading.Thread(target=self.w_present_thread)
        self.w_cmd_thread = threading.Thread(target=self.w_cmd_thread)

        self.active = True

        self.p_min = 0.0
        self.p_max = 1.0

        self.i_min = 0.0
        self.i_max = 1.0

        self.w_min = -20.0
        self.w_max = 20.0

    def wait_until_visible(self):
        while not self.pid_tune_window.isVisible():
            time.sleep(0.1)

    def setupUi(self, pid_tune_window):
        super().setupUi(pid_tune_window)
        self.pid_tune_window = pid_tune_window
        self.p_slider.valueChanged.connect(self.on_p_slider_change)
        self.i_slider.valueChanged.connect(self.on_i_slider_change)
        self.w_slider.valueChanged.connect(self.on_w_slider_change)
        self.stop_button.clicked.connect(self.on_stop)
        self.init_thread.start()
        self.w_present_thread.start()
        self.w_cmd_thread.start()

    def init_thread(self):
        self.wait_until_visible()
        p_init = False
        i_init = False
        self.mobot.write(bytes(f"PCMD:GET\r", 'utf-8'))
        self.mobot.write(bytes(f"ICMD:GET\r", 'utf-8'))
        while not (p_init and i_init):
            msg = self.mobot.readline().decode("utf-8")
            msg_split = msg.split(':')
            if msg_split[0] == 'P':
                p = float(msg_split[1])
                value = p * (1000/(self.p_max-self.p_min))
                self.p_slider.setValue(value)
                p_init = True
            elif msg_split[0] == 'I':
                i = float(msg_split[1])
                value = i * (1000/(self.i_max-self.i_min))
                self.i_slider.setValue(value)
                i_init = True

    def w_present_thread(self):
        self.init_thread.join()
        while self.pid_tune_window.isVisible():
            msg = self.mobot.readline().decode("utf-8")
            msg_split = msg.split(':')
            if msg_split[0] == 'W':
                w = float(msg_split[1])
                w = "{:.2f}".format(w)
                self.w_present_value.setText(f"abs(W): {w} rad/sec")

    def on_p_slider_change(self):
        value = self.p_slider.value() / (1000/(self.p_max-self.p_min))
        self.p_value.setText(str(value))
        self.mobot.write(bytes(f"PCMD:{value}\r", 'utf-8'))

    def on_i_slider_change(self):
        value = self.i_slider.value() / (1000/(self.i_max-self.i_min))
        self.i_value.setText(str(value))
        self.mobot.write(bytes(f"ICMD:{value}\r", 'utf-8'))

    def on_w_slider_change(self):
        value = self.w_slider.value() / (2000/(self.w_max-self.w_min))
        self.w_value.setText(str(value))

    def w_cmd_thread(self):
        rate = Rate(10)
        while self.active:
            value = self.w_slider.value() / (2000/(self.w_max-self.w_min))
            self.mobot.write(bytes(f"WCMD:{value}\r", 'utf-8'))
            rate.sleep()

    def on_stop(self):
        self.w_slider.setValue(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pid_tune_window = QtWidgets.QMainWindow()
    try:
        pid_tune = PIDTune()
    except serial.serialutil.SerialException:
        print("No Serial Device Found!")
        sys.exit()
    pid_tune.setupUi(pid_tune_window)
    pid_tune_window.show()
    if not app.exec_():
        pid_tune.active = False
        sys.exit()
