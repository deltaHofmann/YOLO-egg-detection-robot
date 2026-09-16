from ultralytics import YOLO


class EggDetector:

    def __init__(self, model_path, confidence_threshold=0.8):

        self.model = YOLO(model_path)

        self.confidence_threshold = confidence_threshold
        self.class_names = self.model.names

        print("Model loaded")
        print("Classes:", self.class_names)

    def detect_best(self, image):

        results = self.model(
            image,
            stream=True,
            conf=self.confidence_threshold
        )

        best_box = None
        best_confidence = 0.0

        for result in results:

            for box in result.boxes:

                confidence = float(box.conf[0])

                if confidence > best_confidence:

                    best_confidence = confidence
                    best_box = box

        return best_box