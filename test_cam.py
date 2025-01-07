import cv2

cap = cv2.VideoCapture(0)

state, img = cap.read()
assert state, 'no image'
print(img)
cv2.imwrite('img.jpg', img)