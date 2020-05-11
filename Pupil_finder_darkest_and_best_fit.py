
# First we import all necessary libraries
import cv2
import copy
import Slider
import operator
import numpy as np
import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt
import Small_Functions as sf

# State if you want the feed from a camera or from a steady image
Camera = True

# This is used to initiate the GUI
app = QApplication(sys.argv)

# We define the sliders we want to calibrate the software with the Slider class created in the Slider.py script
Erode_kernel = Slider.Slider('Erode_kernel',1,100,Starting_value=20)                                                # 0
Erode_iterations = Slider.Slider('Erode_iterations',1,20,Starting_value=1)                                                # 1
Canny_threshold_1 = Slider.Slider('Canny_threshold_1',0,300,Starting_value=27)                                # 2
Canny_threshold_2 = Slider.Slider('Canny_threshold_2',0,300,Starting_value=17)                                # 3
Binary_threshold_low = Slider.Slider('Binary_threshold_low',0,255,Starting_value=43)                                # 4
Binary_threshold_high = Slider.Slider('Binary_threshold_high',0,255,Starting_value=255)                                # 5


# Now we define the main window with all the desired sliders as a list
Slider_list = Slider.Slider_window([Erode_kernel,Erode_iterations,Canny_threshold_1,Canny_threshold_2,Binary_threshold_low,Binary_threshold_high])

# We read an image example to work but this should be commented when working with the real camera and we also grayscale it so that it is easier to process
if not Camera:
    img = cv2.imread('Eye_00001.png',cv2.IMREAD_COLOR)
    grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# We assign the camera feed to a variable to treat it and use it afterwards
if Camera:
    cap = cv2.VideoCapture('Eye_video.mp4')

# We show the Slider window
Slider_list.show()

# We define the kernel that will be used on the erode dilate and derivate operations


# We loop infinitely through the camera feed or through the same image to adjust the computation parameters
while True:
    # Timer_1 = sf.Timer()                      # We start a timer to see the elapsed time

    # We take a frame from the feed and process it. First we grayscale it so that it is easier to process
    if Camera:
        ret, img = cap.read()
        grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayscaled = cv2.flip(grayscaled,0)

    glare_kernel = np.ones((Slider_list.Slider_list[0].value(), Slider_list.Slider_list[0].value()), np.uint8)

    eroded = cv2.morphologyEx(grayscaled,cv2.MORPH_OPEN,glare_kernel,borderType=cv2.MORPH_ELLIPSE,iterations=Slider_list.Slider_list[1].value())

    __,binary = cv2.threshold(eroded, Slider_list.Slider_list[4].value(), Slider_list.Slider_list[5].value(), cv2.THRESH_BINARY)

    edges_canny = cv2.Canny(eroded, Slider_list.Slider_list[2].value(), Slider_list.Slider_list[3].value(), )

    contours_canny, hierarchy = cv2.findContours(edges_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    Img_with_canny_contours = copy.copy(eroded)

    cv2.drawContours(Img_with_canny_contours, contours_canny, contourIdx=-1, thickness=1, color=(255, 255, 255))

    h1 = np.hstack((grayscaled,binary))
    h2 = np.hstack((edges_canny,binary))
    res = np.vstack((h1,h2))
    cv2.imshow('image',res)

    key = cv2.waitKey(40)

    # Timer_1.Update_elapsed_time(Print_elapsed_time=True,Precise_time=True)
    if key == 27:
        break
cv2.destroyAllWindows()
sys.exit(app.exec_())
