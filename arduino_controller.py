import serial
import time


class ArduinoController:

    def __init__(self, port, baudrate=9600):
        self.arduino = serial.Serial(
            port,
            baudrate,
            timeout=1
        )

        # Arduino Nano resets when serial connection is opened
        time.sleep(2)

        print("Arduino connected")

    def send_command(self, command):
        self.arduino.write(
            (command + "\n").encode()
        )

    def stop(self):
        print("Stopping motors...")

        self.send_command("N")
        self.arduino.flush()

        time.sleep(0.1)

    def close(self):
        self.stop()
        self.arduino.close()