import time
import keyboard

from arduino_controller import ArduinoController
from config import ARDUINO_PORT, ARDUINO_BAUDRATE


def main():

    arduino = ArduinoController(
        ARDUINO_PORT,
        ARDUINO_BAUDRATE
    )

    print()
    print("Keyboard control:")
    print("W = forward")
    print("A = turn left")
    print("D = turn right")
    print("S = stop")
    print("Q = quit")
    print()

    try:

        while True:

            if keyboard.is_pressed("w"):
                arduino.send_command("C")
                print("FORWARD")

            elif keyboard.is_pressed("a"):
                arduino.send_command("L")
                print("LEFT")

            elif keyboard.is_pressed("d"):
                arduino.send_command("R")
                print("RIGHT")

            elif keyboard.is_pressed("s"):
                arduino.send_command("N")
                print("STOP")

            elif keyboard.is_pressed("q"):
                break

            time.sleep(0.1)

    finally:

        arduino.close()

        print("Program stopped")


if __name__ == "__main__":
    main()