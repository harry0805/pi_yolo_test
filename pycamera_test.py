import av
import numpy as np
import cv2

# Open the camera using PyAV
camera_index = 0
container = av.open("video=UVC Camera", format="dshow")  # Use appropriate device path for your platform

# Set video stream
# stream = container.streams.video[0]
# stream.pix_fmt = 'gray16le'  # 16-bit grayscale format (adjust if necessary)

for frame in container.decode(video=0):
    # Check the format of the frame
    print(f"Frame: {frame} format: {frame.format.name}")

    # Assuming it's grayscale (you can check its format and handle accordingly)
    if frame.format.name == 'gray16be':  # 14-bit grayscale might be handled as 16-bit for compatibility
        print("Grayscale frame received!")

        # Process the frame (you can access pixel data as a NumPy array if needed)
        frame_data = frame.to_ndarray()

        # Example: Print shape of frame data
        print(frame_data.shape)

cv2.destroyAllWindows()
