
# Import necessary libraries
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import copy
import operator
import math

import Slider
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider

import Small_Functions as sf

# Contour Class# We define a class that will hold the values of the extracted contours
class Contour:
    def __init__(self,Contour):
        self.Contour = Contour
        self.Hull = cv2.convexHull(self.Contour, False)
        self.Area = cv2.contourArea(self.Hull)
        self.Arc_length = cv2.arcLength(self.Contour,False)
        self.Centroid = 0,0

    def FindCentroid(self):
        M = cv2.moments(self.Contour)
        self.Centroid = (int(sf.division_possible_zero(M['m10'],M['m00'])),int(sf.division_possible_zero(M['m01'], M['m00'])))

    def fitEllipse(self):
        self.Ellipse_Centroid = cv2.fitEllipse(self.Contour)[0]

    def ContourApproximation(self):
        self.Epsilon = 0.1 * cv2.arcLength(self.Contour, False)
        self.Approximate_Contour = cv2.approxPolyDP(self.Contour, self.Epsilon, False)


# Slider Stuff # This is used to initiate the GUI
app = QApplication(sys.argv)

# # We define the sliders we want to calibrate the software with the Slider class created in the Slider.py script
# blockSize_slider = Slider.Slider('Block Size',1,800,Starting_value=212)                                                # 0
# Substract_Constant = Slider.Slider('Substract Constant',-2,800,Starting_value=23)                                    # 1
# Pupil_Kernel = Slider.Slider('Pupil_Kernel',1,50,Starting_value=1)                                                  # 2
# Binary_threshold_low = Slider.Slider('Binary_threshold_low',0,255,Starting_value=0)                                 # 3
# Binary_threshold_high = Slider.Slider('Binary_threshold_low',0,255,Starting_value=0)                                # 4
# Pupil_opening_iterations = Slider.Slider('Pupil_opening_iterations',0,20,Starting_value=0)                          # 5
# Canny_threshold_1 = Slider.Slider('Canny_threshold_1',0,300,Starting_value=27)                                # 6
# Canny_threshold_2 = Slider.Slider('Canny_threshold_2',0,300,Starting_value=17)                                # 7
# post_glare_blur_size =  Slider.Slider('post_glare_blur_size',0,50,Starting_value=1)                                # 8
# contour_number_analyzing_selection =  Slider.Slider('contour_number_analyzing_selection',0,50,Starting_value=1)                                # 9
# contour_ellipse_centroid_distance =  Slider.Slider('contour_ellipse_centroid_distance',0,300,Starting_value=1)                                # 10
# contour_number_drawing_selection =  Slider.Slider('contour_number_drawing_selection',0,50,Starting_value=1)                                # 11
#
#
# # Now we define the main window with all the desired sliders as a list
# Slider_list = Slider.Slider_window([blockSize_slider,Substract_Constant,Pupil_Kernel,Pupil_opening_iterations,Binary_threshold_low,Binary_threshold_high,Canny_threshold_1,Canny_threshold_2,post_glare_blur_size,contour_number_analyzing_selection,contour_ellipse_centroid_distance,contour_number_drawing_selection])
#
# # We show the Slider window
# Slider_list.show()

# Camera Stuff # State if you want the feed from a camera or from a steady image
Camera = False

# We read an image example to work but this should be commented when working with the real camera and we also grayscale it so that it is easier to process
if not Camera:
    cap = cv2.VideoCapture('output.avi')

# We assign the camera feed to a variable to treat it and use it afterwards
if Camera:
    cap = cv2.VideoCapture(1)

# Glare Stuff# We define all the needed parameters that might need to change when changing scenarios:
Glare_Gaussian_Block_size = 14
Glare_Gaussian_Constant = -30
Glare_Gaussian_inpaint_radius = 9
Glare_Dilation_Iterations = 6

# We define the kernel that will be used on the erode dilate and derivate operations

glare_kernel = np.ones((3,3),np.uint8)

# Glare Sliders:

Glare_Gaussian_Block_size_Slider = Slider.Slider('Block Size',1,800,Starting_value=Glare_Gaussian_Block_size)                                                # 0
Glare_Gaussian_Constant_Slider = Slider.Slider('Substract Constant',-100,800,Starting_value=Glare_Gaussian_Constant)                                    # 1
Glare_Gaussian_inpaint_radius_Slider = Slider.Slider('Glare_Gaussian_inpaint_radius',1,50,Starting_value=Glare_Gaussian_inpaint_radius)                                                  # 2
Glare_Dilation_Iterations = Slider.Slider('Glare_Dilation_Iterations',0,50,Starting_value=Glare_Dilation_Iterations)                                                  # 2
Glare_Open_Kernel = Slider.Slider('Glare_Open_Kernel',1,50,Starting_value=3)                                                  # 2

# Now we define the main window with all the desired sliders as a list
Slider_list_Glare = Slider.Slider_window([Glare_Gaussian_Block_size_Slider,Glare_Gaussian_Constant_Slider,Glare_Gaussian_inpaint_radius_Slider,Glare_Dilation_Iterations,Glare_Open_Kernel])

# We show the Slider window
Slider_list_Glare.show()


# Binary and Canny Thresholds# We define all the needed parameters for the binary threshold:
Lowest_Value = 127
Highest_Value = 255
Offset_From_Lowest_Value = 10

Canny_X = 0
Canny_Y = 0

Contour_Draw_Number = 10

# Binary Sliders:

Binary_Lowest_Value_Slider = Slider.Slider('Lowest Value',0,255,Starting_value=Lowest_Value)
Binary_Highest_Value_Slider = Slider.Slider('Highest Value',0,255,Starting_value=Highest_Value)
Binary_Offset_From_Lowest_Value_Slider = Slider.Slider('Offset From Lowest Value',0,255,Starting_value=Offset_From_Lowest_Value)

Canny_X_Value_Slider = Slider.Slider('Canny X Value ',0,255,Starting_value=Canny_X)
Canny_Y_Value_Slider = Slider.Slider('Canny Y Value ',0,255,Starting_value=Canny_Y)

Contour_Draw_Number_Slider = Slider.Slider('Contour Draw Number',0,255,Starting_value=Contour_Draw_Number)

# Now we define the main window with all the desired sliders as a list
Slider_list_BnC = Slider.Slider_window([Binary_Lowest_Value_Slider,Binary_Highest_Value_Slider,Binary_Offset_From_Lowest_Value_Slider,Canny_X_Value_Slider,Canny_Y_Value_Slider,Contour_Draw_Number_Slider])

# We show the Slider window
Slider_list_BnC.show()

# We define the maximum pupil size to reduce the amount of processing
Max_Pupil_Size = 50

while True:
    # Timer_1 = sf.Timer()                      # We start a timer to see the elapsed time

    # We take a frame from the feed and process it. First we grayscale it so that it is easier to process
    ret, img = cap.read()

    while True:

        # We first convert the image to grayscale
        grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Correct Glare #Then using an adaptative threshold we search for the glare regions where the pupil is reflecting the leds
        glare_gaussian_threshold = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, Slider_list_Glare.Slider_list[0].value()*2+1, Slider_list_Glare.Slider_list[1].value())

        # We define the opening kernel size
        glare_kernel = np.ones(( Slider_list_Glare.Slider_list[4].value(),  Slider_list_Glare.Slider_list[4].value()), np.uint8)
        # Now we 'open' the image to erase any noise and we dilate the remaining points to make sure we are taking the whole glared area
        glare_opening = cv2.morphologyEx(glare_gaussian_threshold, cv2.MORPH_OPEN, glare_kernel)
        glare_dilation = cv2.dilate(glare_opening, glare_kernel, iterations=Slider_list_Glare.Slider_list[3].value())

        # Now with the generated mask we inpaint the original grayscaled frame to fully erase the glare
        glare_Corrected_gaussian = cv2.inpaint(grayscaled, glare_dilation, Slider_list_Glare.Slider_list[2].value(), cv2.INPAINT_TELEA)

        # Find Darkest Region        # Find Darkest region (pupil region)

        Image_Array = glare_Corrected_gaussian.flatten()
        Darkest_Pixel_Value = min(Image_Array)
        #print(Darkest_Pixel_Value)

        _, Darkest_Region = cv2.threshold(glare_Corrected_gaussian, Darkest_Pixel_Value + Slider_list_BnC.Slider_list[2].value(),  Slider_list_BnC.Slider_list[1].value(), cv2.THRESH_BINARY)

        Edges_Canny = cv2.Canny(Darkest_Region, Slider_list_BnC.Slider_list[3].value(), Slider_list_BnC.Slider_list[4].value())

        Darkest_Region_Contours, hierarchy = cv2.findContours(Edges_Canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        Darkest_Contour = list()
        for i,contour in enumerate(Darkest_Region_Contours):
            Darkest_Contour.append(Darkest_Region_Contours[i].tolist())

        Darkest_Contour_Flat = list()
        for sublist in Darkest_Contour:
            for item in sublist:
                Darkest_Contour_Flat.append(item)

        print(*Darkest_Contour_Flat,sep="\n")
        print("------------------------------")

        # Canny_Contour_list.sort(key=operator.attrgetter('Arc_length'), reverse=True)
        #
        # Contour_Draw_Count = Slider_list_BnC.Slider_list[5].value()
        #
        # Canny_Contour_list[0].FindCentroid()
        # print(Canny_Contour_list[0].Centroid)

        Longest_Contour_list = list()

        Rounded_contours = copy.copy(glare_Corrected_gaussian)

        # for i in range(Contour_Draw_Count):
        #     # Canny_Contour_list[i].fitEllipse()
        #     # Canny_Contour_list[i].ContourApproximation()
        #     Longest_Contour_list.append(Canny_Contour_list[i])
        #     cv2.drawContours(glare_Corrected_gaussian, Longest_Contour_list[i].Contour, contourIdx=-1, thickness=2, color=(0, 255, 255))

            # print(Longest_Contour_list[i].Contour)

        # Stack images and Display # We finally stack all the images we have created to see them propperly
        h1 = np.hstack((grayscaled,Edges_Canny))
        h2 = np.hstack((glare_Corrected_gaussian,Rounded_contours))
        res = np.vstack((h1,h2))
        cv2.imshow('image',res)

        # time.sleep(0.01)
        if cv2.waitKey(1) & 0xFF == ord('n') or Camera:
            break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
