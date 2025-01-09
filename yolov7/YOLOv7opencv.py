from yolov7.YOLOv7 import YOLOv7 as YOLOv7Orignal

import cv2
import time
import numpy as np

class YOLOv7(YOLOv7Orignal):
    def __init__(self, path, conf_thres=0.7, iou_thres=0.5, official_nms=False):
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.official_nms = official_nms

        # Initialize model
        self.initialize_model(path)

    def initialize_model(self, path):
        self.net = cv2.dnn.readNetFromONNX(path)
        # Get model info
        self.get_input_details()
        self.get_output_details()

        self.has_postprocess = 'score' in self.output_names or self.official_nms

    def get_input_details(self):
        # Set input height and width based on the model's expected input size
        self.input_height = 480  # Replace with your model's expected input height
        self.input_width = 640   # Replace with your model's expected input width

        # Get the names of all layers (not typically needed for input details)
        self.input_names = self.net.getLayerNames()

    def get_output_details(self):
        # Get the names of the output layers
        self.output_names = self.net.getUnconnectedOutLayersNames()
    
    def inference(self, input_tensor):
        start = time.perf_counter()

        # Ensure the input tensor is in the correct format
        # OpenCV expects the input to be a blob with shape [batch_size, channels, height, width]
        # and type np.float32
        if input_tensor.dtype != np.float32:
            input_tensor = input_tensor.astype(np.float32)

        # Set the input to the network
        self.net.setInput(input_tensor)

        # Perform forward pass to get outputs
        # If there are multiple outputs, outputs will be a dict with layer names as keys
        outputs = self.net.forward(self.output_names)

        print(f"Inference time: {(time.perf_counter() - start)*1000:.2f} ms")
        return outputs