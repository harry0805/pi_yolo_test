import cv2

cap = cv2.VideoCapture(0)

state, img = cap.read()
cv2.imwrite('img.jpg', img)
print(img)