import cv2


def calculate_target_position(
    box,
    image_width,
    image_height,
    middle_threshold
):

    x1, y1, x2, y2 = box.xyxy[0]

    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    image_center_x = image_width // 2
    image_center_y = image_height // 2

    relative_x = center_x - image_center_x
    relative_y = image_center_y - center_y

    if relative_x > middle_threshold:
        command = "R"

    elif relative_x < -middle_threshold:
        command = "L"

    else:
        command = "C"

    confidence = float(box.conf[0])

    class_id = int(box.cls[0])

    return {
        "box": (x1, y1, x2, y2),
        "center": (center_x, center_y),
        "relative_position": (relative_x, relative_y),
        "confidence": confidence,
        "class_id": class_id,
        "command": command
    }


def draw_detection(
    image,
    detection,
    class_name
):

    x1, y1, x2, y2 = detection["box"]

    center_x, center_y = detection["center"]

    relative_x, relative_y = detection["relative_position"]

    confidence = detection["confidence"]

    command = detection["command"]


    # Bounding box

    cv2.rectangle(
        image,
        (x1, y1),
        (x2, y2),
        (255, 0, 255),
        3
    )


    # Center point

    cv2.circle(
        image,
        (center_x, center_y),
        5,
        (0, 0, 255),
        -1
    )


    # Label

    cv2.putText(
        image,
        f"{class_name} {confidence:.2f}",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2
    )


    # Relative coordinates

    cv2.putText(
        image,
        f"({relative_x}, {relative_y})",
        (x1, y2 + 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    # Command

    cv2.putText(
        image,
        f"Command: {command}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )


def draw_no_detection(image):

    cv2.putText(
        image,
        "No detection",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )


def draw_image_center(image):

    image_center_x = image.shape[1] // 2
    image_center_y = image.shape[0] // 2

    cv2.drawMarker(
        image,
        (image_center_x, image_center_y),
        (0, 255, 0),
        cv2.MARKER_CROSS,
        20,
        2
    )