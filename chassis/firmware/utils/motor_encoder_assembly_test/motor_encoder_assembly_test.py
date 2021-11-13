import math
import sys
import threading, time
import serial
from PyQt5 import QtCore, QtGui, QtWidgets

from ui_motor_encoder_assembly_test import Ui_motor_encoder_assembly_test

class MotorEncoderAssemblyTest(Ui_motor_encoder_assembly_test):
    def __init__(self):
        super().__init__()
        self.mobot = serial.Serial(port='/dev/ttyUSB0',\
                                   baudrate=115200,\
                                   timeout=1)
        self.encoder_read_thread = threading.Thread(target=self.encoder_read_thread)

    def setupUi(self, motor_encoder_assembly_test_window):
        super().setupUi(motor_encoder_assembly_test_window)
        self.motor_encoder_assembly_test_window = motor_encoder_assembly_test_window
        self.motor_cmd_slider.valueChanged.connect(self.on_motor_cmd_slider_change)
        self.motor_stop.clicked.connect(self.on_motor_stop)
        self.encoder_read_thread.start()

    def encoder_read_thread(self):
        ## Wait until visible
        while not self.motor_encoder_assembly_test_window.isVisible():
            time.sleep(0.1)

        while self.motor_encoder_assembly_test_window.isVisible():
            msg = self.mobot.readline().decode("utf-8")
            msg_split = msg.split(':')
            if msg_split[0] == 'ENC':
                ticks = int(msg_split[1])
                rad = float(msg_split[2])
                deg = "{:.2f}".format(rad * (180.0/math.pi))
                self.encoder_ticks.setText(f"{ticks} Ticks")
                self.encoder_deg.setText(f"{deg} Deg")

                w = float(msg_split[3])
                rps = "{:.3f}".format(w)
                rpm = "{:.2f}".format(w * (60.0/(2 * math.pi)))
                self.encoder_rps.setText(f"{rps} Rad/s")
                self.encoder_rpm.setText(f"{rpm} RPM")

    def on_motor_cmd_slider_change(self):
        value = self.motor_cmd_slider.value() / 1000
        self.motor_cmd.setText(str(value))
        self.mobot.write(bytes(f"CMD:{value}\r", 'utf-8'))

    def on_motor_stop(self):
        self.motor_cmd_slider.setValue(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    motor_encoder_assembly_test_window = QtWidgets.QMainWindow()
    try:
        motor_encoder_assembly_test = MotorEncoderAssemblyTest()
    except serial.serialutil.SerialException:
        print("No Serial Device Found!")
        sys.exit()
    motor_encoder_assembly_test.setupUi(motor_encoder_assembly_test_window)
    motor_encoder_assembly_test_window.show()
    sys.exit(app.exec_())
