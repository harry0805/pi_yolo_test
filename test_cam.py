import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, 40) 

state, img = cap.read()
print(img.depth())


# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite('img.jpg', img)
assert state, 'no image'
print(img)

while True:
    try:
        state, img = cap.read()
        assert state, 'no image'
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Camera', img)
        cv2.waitKey(1)
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        quit()
