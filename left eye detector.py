import cv2
import numpy as np

eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
eye_cascade2 = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    grayf = cv2.flip(gray, -1)
    eyes = eye_cascade.detectMultiScale(grayf, 1.3, 5)
    for (x,y,w,h) in eyes:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow("frame",frame)
    cv2.imshow("frame", grayf)

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
