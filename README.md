# YOLO Egg Detection Robot

A small autonomous robot that uses a camera, a YOLO object detection model, an Arduino, DC gear motors and an ultrasonic distance sensor to detect and follow an egg.

The project combines computer vision with embedded motor control. The camera is used to determine the position of the egg in the image, while an ultrasonic sensor measures the distance to the object.

---

## Features

- Real-time egg detection using YOLO
- Detection of white and brown eggs
- USB webcam input
- Arduino-based motor control
- HC-SR04 ultrasonic distance sensor
- Automatic left/right steering based on the egg position
- Distance-based control to prevent the robot from getting too close
- Manual motor testing using the keyboard
- Modular Python structure separating detection, vision and hardware control

---

## How It Works

The robot consists of two main systems:

### 1. Computer Vision

A webcam continuously captures images of the environment.

The YOLO model detects eggs in the camera image and determines their bounding boxes. The detection with the highest confidence is selected as the target.

The center of the detected bounding box is compared with the center of the camera image:

- Egg is left of the center → turn left
- Egg is right of the center → turn right
- Egg is approximately centered → move forward

A configurable threshold is used to define the central region.

### 2. Distance Measurement

An HC-SR04 ultrasonic sensor is used to measure the distance between the robot and the object in front of it.

The ultrasonic sensor sends an ultrasonic pulse and measures the time required for the reflected signal to return. From this time, the distance can be calculated.

The distance information is used to prevent the robot from driving too close to the egg.

This separates the two tasks:

| Component | Function |
|---|---|
| Webcam | Provides the camera image |
| YOLO | Detects the egg and its position |
| HC-SR04 | Measures the distance to the object |
| Python | Processes detections and controls the robot |
| Arduino Nano | Receives commands and controls the motors |
| L9110S | Drives the DC motors |
| DC gear motors | Move the robot |

---

## Project Structure

```text
YOLO-egg-detection-robot/
│
├── main.py
├── motor_test.py
├── config.py
├── detector.py
├── vision.py
├── arduino_controller.py
│
├── arduino/
│   └── egg_following_robot/
│       └── egg_following_robot.ino
│
├── models/
│   └── best.pt
│
├── images/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Hardware

The robot uses the following components:

- Arduino Nano
- USB webcam
- HC-SR04 ultrasonic distance sensor
- L9110S dual motor driver
- 2 × TT DC gear motors
- Robot chassis and wheels
- Battery supply for the motors
- Computer running Python and YOLO


## Mechanical Design & Inspiration

The mechanical design of the robot was inspired by the following MakerWorld project:

[Quadrupedal Walking Mechanism](https://makerworld.com/de/models/1511692-quadrupedal-walking-mechanism?from=search#profileId-1583010)

The original design was adapted for this project to accommodate the two-motor drive system.

The main modifications are:

- The motor mount was mirrored to allow two motors to be installed.
- Each motor drives its own separate gear.
- Two separate crankshafts are used to transfer the motor rotation to the walking mechanism.
- The mechanical layout was adapted to integrate the electronics, motors and autonomous control system.

The resulting robot combines the mechanical walking mechanism inspired by the original MakerWorld design with a custom computer-vision and control system based on YOLO, Arduino and an HC-SR04 ultrasonic sensor.


### Motor System

The two TT gear motors are controlled using an L9110S motor driver.

The Arduino receives simple movement commands from the Python program:

| Command | Function |
|---|---|
| `C` | Move forward |
| `L` | Turn left |
| `R` | Turn right |
| `N` | Stop |

The Python program does not directly control the motors. Instead, it sends these commands over a serial connection to the Arduino.

---

## Wiring

### HC-SR04

The ultrasonic sensor is connected to the Arduino as follows:

| HC-SR04 | Arduino Nano |
|---|---|
| VCC | 5V |
| GND | GND |
| TRIG | D6 |
| ECHO | A7 |

### L9110S Motor Driver

The current motor control setup uses:

| L9110S | Arduino Nano |
|---|---|
| B-1A | D2 |
| B-2A | D3 |
| A-1A | D4 |
| A-1B | D5 |
| VIN | Motor power supply |

The exact motor power supply should be chosen according to the motors and motor driver being used.

---

## Software

The project uses Python for the computer vision and high-level robot control.

Main Python components:

- Python
- Ultralytics YOLO
- OpenCV
- PySerial
- keyboard

### Python Files

#### `main.py`

Main program of the robot.

It:

1. Opens the webcam
2. Loads the YOLO model
3. Detects eggs in each frame
4. Determines the egg position
5. Generates a movement command
6. Sends the command to the Arduino
7. Displays the detection result

#### `detector.py`

Contains the YOLO-based egg detection logic.

The program uses the detection with the highest confidence as the current target.

#### `vision.py`

Contains image-processing and visualization functions.

It calculates:

- Bounding box coordinates
- Egg center position
- Relative position to the camera center
- Movement command

It also draws the detection information onto the camera image.

#### `arduino_controller.py`

Handles the serial connection to the Arduino.

It is responsible for:

- Opening the serial connection
- Sending movement commands
- Stopping the motors
- Closing the connection safely

#### `config.py`

Contains the main configuration parameters, such as:

```python
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

ARDUINO_PORT = "COM3"
ARDUINO_BAUDRATE = 9600

MODEL_PATH = "models/best.pt"
CONFIDENCE_THRESHOLD = 0.8

MIDDLE_THRESHOLD = 50
```

These values can be changed without modifying the main program.

#### `motor_test.py`

Provides a simple manual control mode for testing the motors.

Keyboard controls:

| Key | Command |
|---|---|
| `W` | Forward |
| `A` | Left |
| `D` | Right |
| `S` | Stop |
| `Q` | Quit |

---

## YOLO Model

The robot uses a custom-trained YOLO object detection model.

The trained model is stored in:

```text
models/best.pt
```

The model is loaded using the Ultralytics YOLO framework.

The current detection threshold is:

```text
0.8
```

Only detections with a confidence of at least 0.8 are considered.

---

## Dataset

The YOLO model was trained using the publicly available **Egg Detection** dataset by `afshin-dini`.

The dataset contains two egg classes:

- `white-egg`
- `brown-egg`

The dataset uses YOLO-style bounding-box annotations and contains training and validation data.

The dataset is licensed under the MIT License.

The dataset is **not included in this repository**.

If you want to reproduce the model training, download the dataset from the original source:

[Egg Detection Dataset](https://huggingface.co/datasets/afshin-dini/Egg-Detection)

---

## Installation

### Install Dependencies

### Connect the Arduino

Connect the Arduino Nano to the computer via USB.

Check which COM port is assigned to the Arduino.

The default configuration uses:

```python
ARDUINO_PORT = "COM3"
```

If a different COM port is assigned, change it in `config.py`.

For example:

```python
ARDUINO_PORT = "COM5"
```

### Upload the Arduino Program

Open the Arduino sketch located at:

```text
arduino/egg_following_robot/egg_following_robot.ino
```

Open it using the Arduino IDE and upload it to the Arduino Nano.

Make sure that the Arduino pins used in the sketch match the physical wiring.

---

## Running the Robot

After connecting the Arduino, webcam and robot hardware, run:

```bash
python main.py
```

The program will:

1. Connect to the Arduino
2. Open the webcam
3. Load the YOLO model
4. Start detecting eggs
5. Determine the egg's position
6. Send movement commands to the Arduino
7. Display the camera image and detection information

Press:

```text
Q
```

to stop the program.

When the program exits, it sends a stop command to the Arduino before closing the serial connection.

---

## Motor Test

Before running the autonomous system, the motors can be tested manually.

Run:

```bash
python motor_test.py
```

Then use:

```text
W = forward
A = left
D = right
S = stop
Q = quit
```

This allows the motor control and Arduino communication to be tested independently of the YOLO system.

---

## Detection Logic

The camera resolution is currently set to:

```text
640 × 480
```

The center of the camera image is therefore approximately:

```text
(320, 240)
```

The center of the detected egg is compared with the image center.

For the horizontal position, a configurable threshold is used:

```python
MIDDLE_THRESHOLD = 50
```

This creates a central region in which the robot is considered aligned with the egg.

Simplified control logic:

```text
                 Camera
        ┌─────────────────────┐
        │                     │
        │    LEFT   CENTER   RIGHT
        │      ←      ↓       →
        │             ●       │
        │          Egg        │
        │                     │
        └─────────────────────┘
```

The current system mainly uses the horizontal position for steering.

The HC-SR04 provides additional distance information for controlling how close the robot approaches the egg.

---

## Communication

Python communicates with the Arduino through a serial connection.

Current settings:

```text
Port: COM3
Baud rate: 9600
```

Commands are sent as single characters followed by a newline:

```text
C
L
R
N
```

This keeps the communication between the computer and Arduino simple and easy to debug.

---

## Safety and Error Handling

The program includes basic handling for common failures.

If the webcam cannot be opened, the program stops and closes the Arduino connection.

When the program is terminated, a stop command is sent to the Arduino:

```text
N
```

This prevents the motors from continuing to run after the Python program has stopped.

---

## Limitations

This is a V1 prototype and has several limitations:

- The robot currently relies on a single webcam for visual detection.
- YOLO performance depends on lighting, camera angle and the appearance of the egg.
- The robot selects the highest-confidence egg detection as its target.
- The current steering logic is based primarily on the horizontal image position.
- Ultrasonic distance measurements can be affected by the angle and surface of the detected object.
- The robot does not yet perform advanced path planning or obstacle avoidance.
- The system requires a computer to run the YOLO model.

---

## Future Improvements

Possible improvements include:

- More robust distance-based control
- Smoother motor control
- Proportional steering instead of simple left/right commands
- Obstacle detection and avoidance
- Improved camera mounting
- Additional training data
- Model optimization for faster inference
- Running the vision system on an embedded computer
- Automatic stopping when the egg reaches a defined distance
- Improved handling of multiple detected eggs

---

## Author

**deltaHofmann**

This project was developed as a practical project combining:

- Computer Vision
- Machine Learning
- Python
- Embedded Systems
- Arduino
- Robotics