import cv2

# Open the camera
camera_index = 0  # Change if multiple cameras are connected
cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Use CAP_DSHOW for Windows

# Set resolution (if needed)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Replace with your camera's width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Replace with your camera's height

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Check if the camera supports 14-bit data output
    # frame might come in 16-bit format if 14-bit isn't directly supported
    if frame.dtype == 'uint16':  # Most 14-bit cameras use uint16 containers
        # Normalize 14-bit data for visualization or processing
        # 14-bit data ranges from 0 to 16383
        frame_normalized = (frame / 16383.0 * 255).astype('uint8')  # Convert to 8-bit for display

        # Display the frame (optional)
        cv2.imshow('14-bit Grayscale Camera', frame_normalized)

    else:
        print("Unexpected frame format:", frame.dtype)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
