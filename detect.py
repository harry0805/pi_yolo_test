import argparse
import cv2.dnn
import numpy as np
from pathlib import Path
import re
import yaml

def yaml_load(file="data.yaml", append_filename=False):
    """
    Load YAML data from a file.

    Args:
        file (str, optional): File name. Default is 'data.yaml'.
        append_filename (bool): Add the YAML filename to the YAML dictionary. Default is False.

    Returns:
        dict: YAML data and file name.
    """
    assert Path(file).suffix in {".yaml", ".yml"}, f"Attempting to load non-YAML file {file} with yaml_load()"
    with open(file, errors="ignore", encoding="utf-8") as f:
        s = f.read()  # string

        # Remove special characters
        if not s.isprintable():
            s = re.sub(
                r"[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+", "", s
            )

        # Add YAML filename to dict and return
        data = yaml.safe_load(s) or {}  # always return a dict
        if append_filename:
            data["yaml_file"] = str(file)
        return data

class ObjectDetector:
    def __init__(self, model_path, class_file_path):
        """
        Initializes the ObjectDetector with the given model and class file paths.

        Args:
            model_path (str): Path to the ONNX model file.
            class_file_path (str): Path to the YAML file containing class names.
        """
        # Load the ONNX model
        self.model = cv2.dnn.readNetFromONNX(model_path)

        # Load class names from YAML file
        self.CLASSES = yaml_load(class_file_path)["names"]
        np.random.seed(42)
        self.colors = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))

    def load_image(self, image_path):
        """
        Loads an image from the given path and prepares it for inference.

        Args:
            image_path (str): Path to the input image.
        """
        self.original_image = cv2.imread(image_path)
        height, width, _ = self.original_image.shape

        # Prepare a square image by padding if necessary
        length = max(height, width)
        self.image = np.zeros((length, length, 3), np.uint8)
        self.image[0:height, 0:width] = self.original_image

        # Calculate scale factor
        self.scale = length / 640

    def preprocess(self):
        """
        Preprocesses the image and prepares the blob for model input.

        Returns:
            numpy.ndarray: The preprocessed blob.
        """
        # Prepare blob for model input
        blob = cv2.dnn.blobFromImage(
            self.image,
            scalefactor=1 / 255,
            size=(640, 640),
            swapRB=True,
        )
        return blob

    def inference(self, blob):
        """
        Performs inference on the preprocessed blob.

        Args:
            blob (numpy.ndarray): The preprocessed blob.

        Returns:
            numpy.ndarray: The model outputs.
        """
        self.model.setInput(blob)
        outputs = self.model.forward()
        return outputs

    def postprocess(self, outputs):
        """
        Processes the model outputs, applies NMS, and prepares detections.

        Args:
            outputs (numpy.ndarray): The model outputs.

        Returns:
            list: List of dictionaries containing detection information.
        """
        # Prepare output array
        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []

        # Iterate through output to collect bounding boxes, confidence scores, and class IDs
        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            _, maxScore, _, maxClassIndex = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                x, y, w, h = (
                    outputs[0][i][0],
                    outputs[0][i][1],
                    outputs[0][i][2],
                    outputs[0][i][3],
                )
                left = x - 0.5 * w
                top = y - 0.5 * h
                box = [left, top, w, h]
                boxes.append(box)
                scores.append(float(maxScore))
                class_ids.append(int(maxClassIndex[1]))

        # Apply NMS (Non-maximum suppression)
        indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold=0.25, nms_threshold=0.45)

        detections = []

        if len(indices) > 0:
            for i in indices.flatten():
                box = boxes[i]
                detection = {
                    "class_id": class_ids[i],
                    "class_name": self.CLASSES[class_ids[i]],
                    "confidence": scores[i],
                    "box": box,
                    "scale": self.scale,
                }
                detections.append(detection)
        return detections

    def draw_boxes(self, detections):
        """
        Draws bounding boxes and labels on the original image based on the detections.

        Args:
            detections (list): List of detection dictionaries.
        """
        for detection in detections:
            class_id = detection["class_id"]
            confidence = detection["confidence"]
            x = round(detection["box"][0] * detection["scale"])
            y = round(detection["box"][1] * detection["scale"])
            x_plus_w = round((detection["box"][0] + detection["box"][2]) * detection["scale"])
            y_plus_h = round((detection["box"][1] + detection["box"][3]) * detection["scale"])
            label = f"{self.CLASSES[class_id]} ({confidence:.2f})"
            color = self.colors[class_id]
            cv2.rectangle(self.original_image, (x, y), (x_plus_w, y_plus_h), color, 2)
            cv2.putText(
                self.original_image,
                label,
                (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2,
            )

    def detect(self, image_path):
        """
        Full detection pipeline on the input image.

        Args:
            image_path (str): Path to the input image.

        Returns:
            list: List of detection dictionaries.
        """
        self.load_image(image_path)
        blob = self.preprocess()
        outputs = self.inference(blob)
        detections = self.postprocess(outputs)
        self.draw_boxes(detections)
        return detections

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default="models/moose_20240125_mAP50-0.992.onnx",
        help="Path to your ONNX model.",
    )
    parser.add_argument("--img", default="moose-1.jpg", help="Path to input image.")
    parser.add_argument(
        "--classes", default="dataset.yaml", help="Path to class names YAML file."
    )
    args = parser.parse_args()

    from tqdm import tqdm

    # Initialize the detector once to avoid reloading model and classes in each iteration
    detector = ObjectDetector(args.model, args.classes)
    for i in tqdm(range(1000)):
        detections = detector.detect(args.img)
        # Optionally, display or save the result image
        # cv2.imshow("Detections", detector.original_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()