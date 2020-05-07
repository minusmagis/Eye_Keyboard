
# First we import all necessary libraries
import cv2
import Slider
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt
import Small_Functions as sf


app = QApplication(sys.argv)
blockSize_slider = Slider.Slider('Block Size',5,500)
Substract_Constant = Slider.Slider('Substract Constant',-80,80,Starting_value=-20)
Threshold_binary_max = Slider.Slider('Threshold_binary_max',0,255)
Threshold_binary_min = Slider.Slider('Threshold_binary_min',0,255)
Inpaint_Radius = Slider.Slider('Inpaint_Radius',1,300,Starting_value=9)
Slider_list = Slider.Slider_window([blockSize_slider,Substract_Constant,Threshold_binary_max,Threshold_binary_min,Inpaint_Radius])

kernel = np.ones((3,3),np.uint8)

img = cv2.imread('Eye_00001.png',cv2.IMREAD_COLOR)

# cap = cv2.VideoCapture(0)

grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
Slider_list.show()

while True:
    # ret, img = cap.read()
    # grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Timer_1 = sf.Timer()
    # print(Slider_list.Slider_list[1].value())
    # retval, threshold = cv2.threshold(grayscaled, Slider_list.Slider_list[3].value(), Slider_list.Slider_list[2].value(), cv2.THRESH_BINARY)
    th = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY, (Slider_list.Slider_list[0].value()*2+3), Slider_list.Slider_list[1].value())

    # dst = cv2.inpaint(img, threshold, 3, cv2.INPAINT_TELEA)

    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    dilation = cv2.dilate(opening, kernel, iterations=3)

    dst2 = cv2.inpaint(img, dilation, Slider_list.Slider_list[4].value(), cv2.INPAINT_TELEA)

    cv2.imshow('image',img)
    cv2.imshow('Otsu threshold',th)
    cv2.imshow('Otsu threshold open', dilation)
    # cv2.imshow('Corrected binary', dst)
    cv2.imshow('Corrected gaussian', dst2)
    # cv2.imshow('Binary', threshold)

    key = cv2.waitKey(1)

    # Timer_1.Update_elapsed_time(Print_elapsed_time=True,Precise_time=True)
    if key == 27:
        break
cv2.destroyAllWindows()
sys.exit(app.exec_())