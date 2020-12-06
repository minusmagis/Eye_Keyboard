import cv2
import numpy as np


cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FPS, 24)


# cap.set(10, 50  ) # brightness     min: 0   , max: 255 , increment:1
# cap.set(11, 50   ) # contrast       min: 0   , max: 255 , increment:1
# cap.set(12, 70   ) # saturation     min: 0   , max: 255 , increment:1
# cap.set(13, 13   ) # hue
# cap.set(14, 50   ) # gain           min: 0   , max: 127 , increment:1
# cap.set(15, -7   ) # exposure       min: -7  , max: -1  , increment:1
# cap.set(17, 5000 ) # white_balance  min: 4000, max: 7000, increment:1
# cap.set(28, 0    ) # focus          min: 0   , max: 255 , increment:5
fps = int(cap.get(5))
print("fps:", fps)


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    rotated_image = np.rot90(frame)


    cv2.imshow("frame",frame)
    key = cv2.waitKey(1)


    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()