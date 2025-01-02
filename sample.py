import cv2
import numpy as np

cap = cv2.VideoCapture(0)
 
while  True:
    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 19, 0])
    higher_red = np.array([116, 116, 212])

    mask = cv2.inRange(hsv, lower_red,higher_red)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask",mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()