import cv2

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    ARDUINO_PORT,
    ARDUINO_BAUDRATE,
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    MIDDLE_THRESHOLD
)

from detector import EggDetector
from arduino_controller import ArduinoController

from vision import (
    calculate_target_position,
    draw_detection,
    draw_no_detection,
    draw_image_center
)


def main():

    # ==========================================
    # Arduino
    # ==========================================

    arduino = ArduinoController(
        ARDUINO_PORT,
        ARDUINO_BAUDRATE
    )


    # ==========================================
    # Camera
    # ==========================================

    cap = cv2.VideoCapture(CAMERA_INDEX)

    cap.set(3, FRAME_WIDTH)
    cap.set(4, FRAME_HEIGHT)

    if not cap.isOpened():
        arduino.close()
        raise RuntimeError("Could not open webcam")

    print("Webcam is on")


    # ==========================================
    # YOLO
    # ==========================================

    detector = EggDetector(
        MODEL_PATH,
        CONFIDENCE_THRESHOLD
    )


    # ==========================================
    # Main loop
    # ==========================================

    try:

        while True:

            success, image = cap.read()

            if not success:
                print("Could not read frame from webcam")
                break


            # Default command: stop

            command = "N"


            # ======================================
            # Object detection
            # ======================================

            best_box = detector.detect_best(image)


            if best_box is not None:

                detection = calculate_target_position(
                    best_box,
                    image.shape[1],
                    image.shape[0],
                    MIDDLE_THRESHOLD
                )

                command = detection["command"]

                class_id = detection["class_id"]

                class_name = detector.class_names[class_id]


                print("--------------------------------")
                print(f"TARGET: {class_name}")
                print(f"Confidence: {detection['confidence']:.2f}")
                print(
                    f"Position: "
                    f"{detection['relative_position']}"
                )
                print(f"Command: {command}")
                print("--------------------------------")


                draw_detection(
                    image,
                    detection,
                    class_name
                )

            else:

                draw_no_detection(image)


            # ======================================
            # Send command to Arduino
            # ======================================

            arduino.send_command(command)


            # ======================================
            # Visualization
            # ======================================

            draw_image_center(image)

            cv2.imshow(
                "Egg Following Robot",
                image
            )


            # ======================================
            # Quit
            # ======================================

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


    finally:

        # ==========================================
        # Cleanup
        # ==========================================

        cap.release()

        arduino.close()

        cv2.destroyAllWindows()

        print("Program stopped")


if __name__ == "__main__":
    main()