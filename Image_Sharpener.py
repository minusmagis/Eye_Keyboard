import cv2
import Slider
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider

# This is used to initiate the GUI
app = QApplication(sys.argv)

Sharpen_Constant = Slider.Slider('Sharpen_Constant',0,500,Starting_value=0)
Blur_Constant = Slider.Slider('Blur_Constant',0,50,Starting_value=0)
Slider_list = Slider.Slider_window([Sharpen_Constant,Blur_Constant])

Slider_list.show()

#Load source / input image as grayscale, also works on color images...
imgIn = cv2.imread("Eye_00001.png", cv2.IMREAD_GRAYSCALE)

while True:
    blur = cv2.bilateralFilter(imgIn,Slider_list.Slider_list[1].value()+1,75,75)
    sharp = imgIn + (imgIn-blur) * (Slider_list.Slider_list[0].value())

    res = np.hstack((imgIn,blur,sharp))
    cv2.imshow('Image ', res)

    key = cv2.waitKey(1)

    # Timer_1.Update_elapsed_time(Print_elapsed_time=True,Precise_time=True)
    if key == 27:
        break