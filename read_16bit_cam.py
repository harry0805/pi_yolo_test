import cv2
import numpy as np

# Open the camera using the appropriate backend
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'GREY'))

# Check if the camera opened successfully
if not cap.isOpened():
    print("Cannot open camera")
    exit()


# Read and display frames from the camera
while True:
    ret, raw_frame = cap.read()
    if not ret:
        print("Cannot receive frame. Exiting ...")
        break
    
    # split_frame = raw_frame.reshape(512, 320, 2)
    
    # cv2.imshow('Camera Feed', np.hstack((split_frame[:,:,0], split_frame[:,:,1])))

    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()