
# First we import all necessary libraries
import cv2
import copy
import Slider
import operator
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt
import Small_Functions as sf

class Contour:
    def __init__(self,Contour):
        self.Contour = Contour
        self.Hull = cv2.convexHull(self.Contour, False)
        self.Area = cv2.contourArea(self.Hull)
        self.Arc_length = cv2.arcLength(self.Contour,False)
        self.Centroid = 0,0

    def fitEllipse(self):
        self.Centroid = cv2.fitEllipse(self.Contour)[0]

# State if you want the feed from a camera or from a steady image
Camera = True


# This is used to initiate the GUI
app = QApplication(sys.argv)

# We define the sliders we want to calibrate the software with the Slider class created in the Slider.py script
blockSize_slider = Slider.Slider('Block Size',1,100,Starting_value=6)                                                # 0
Substract_Constant = Slider.Slider('Substract Constant',-80,80,Starting_value=4)                                    # 1
Pupil_Kernel = Slider.Slider('Pupil_Kernel',1,50,Starting_value=1)                                                  # 2
Binary_threshold_low = Slider.Slider('Binary_threshold_low',0,255,Starting_value=0)                                 # 3
Binary_threshold_high = Slider.Slider('Binary_threshold_low',0,255,Starting_value=0)                                # 4
Pupil_opening_iterations = Slider.Slider('Pupil_opening_iterations',0,20,Starting_value=0)                          # 5
Canny_threshold_1 = Slider.Slider('Canny_threshold_1',0,300,Starting_value=27)                                # 6
Canny_threshold_2 = Slider.Slider('Canny_threshold_2',0,300,Starting_value=17)                                # 7
post_glare_blur_size =  Slider.Slider('post_glare_blur_size',0,50,Starting_value=1)                                # 8
contour_number_analyzing_selection =  Slider.Slider('contour_number_analyzing_selection',0,50,Starting_value=1)                                # 9
contour_ellipse_centroid_distance =  Slider.Slider('contour_ellipse_centroid_distance',0,300,Starting_value=1)                                # 10
contour_number_drawing_selection =  Slider.Slider('contour_number_drawing_selection',0,50,Starting_value=1)                                # 11


# Now we define the main window with all the desired sliders as a list
Slider_list = Slider.Slider_window([blockSize_slider,Substract_Constant,Pupil_Kernel,Pupil_opening_iterations,Binary_threshold_low,Binary_threshold_high,Canny_threshold_1,Canny_threshold_2,post_glare_blur_size,contour_number_analyzing_selection,contour_ellipse_centroid_distance,contour_number_drawing_selection])

# We define the kernel that will be used on the erode dilate and derivate operations
glare_kernel = np.ones((3,3),np.uint8)

# We read an image example to work but this should be commented when working with the real camera and we also grayscale it so that it is easier to process
if not Camera:
    img = cv2.imread('Eye_00001.png',cv2.IMREAD_COLOR)
    grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# We assign the camera feed to a variable to treat it and use it afterwards
if Camera:
    cap = cv2.VideoCapture(0)

# We show the Slider window
Slider_list.show()

# We define all the needed parameters that might need to change when changing scenarios:
Glare_Gaussian_Block_size = 13
Glare_Gaussian_Constant = -20
Glare_Gaussian_inpaint_radius = 9

# We loop infinitely through the camera feed or through the same image to adjust the computation parameters
while True:
    Timer_1 = sf.Timer()                      # We start a timer to see the elapsed time

    # We take a frame from the feed and process it. First we grayscale it so that it is easier to process
    if Camera:
        ret, img = cap.read()
        grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayscaled = cv2.flip(grayscaled,0)

    # We apply a gaussian threshold to search for the brightest section of the image (the NIR LED glare)
    glare_gaussian_threshold = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY, Glare_Gaussian_Block_size, Glare_Gaussian_Constant)

    # Now we 'open' the image to erase any noise and we dilate the remaining points to make sure we are taking the whole glared area
    glare_opening = cv2.morphologyEx(glare_gaussian_threshold, cv2.MORPH_OPEN, glare_kernel)
    glare_dilation = cv2.dilate(glare_opening, glare_kernel, iterations=2)

    # Now with the generated mask we inpaint the original grayscaled frame to fully erase the glare
    glare_Corrected_gaussian = cv2.inpaint(grayscaled, glare_dilation, Glare_Gaussian_inpaint_radius, cv2.INPAINT_TELEA)

    # print(*Corrected_gaussian_local_blur,sep='\n')
    Post_glare_blur_size = ((Slider_list.Slider_list[8].value() * 2 + 1), (Slider_list.Slider_list[8].value() * 2 + 1))
    glare_Corrected_gaussian_blured = blur = cv2.GaussianBlur(glare_Corrected_gaussian, Post_glare_blur_size, 0)

    edges_canny = cv2.Canny(glare_Corrected_gaussian_blured, Slider_list.Slider_list[6].value(), Slider_list.Slider_list[7].value(),)

    contours_canny, hierarchy = cv2.findContours(edges_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    Img_with_canny_contours = copy.copy(glare_Corrected_gaussian_blured)
    Img_with_only_pupil = copy.copy(glare_Corrected_gaussian_blured)

    canny_contour_list = list()
    # print(len(contours))

    for contour in contours_canny:
        canny_contour_list.append(Contour(contour))

    canny_contour_list.sort(key=operator.attrgetter('Arc_length'),reverse=True)

    contour_draw_count = Slider_list.Slider_list[9].value()
    longest_contour_list = list()

    for i in range(contour_draw_count):
        canny_contour_list[i].fitEllipse()
        longest_contour_list.append(canny_contour_list[i])

    Centroid_acceptable_distance = Slider_list.Slider_list[10].value()

    for i in range(contour_draw_count):
        Main_Centroid_X = int(longest_contour_list[i].Centroid[0])
        Main_Centroid_Y = int(longest_contour_list[i].Centroid[1])
        # print(Main_Centroid_X)
        # print(Main_Centroid_Y)
        for j in range(contour_draw_count):
            if i==j:
                continue
            Temp_Centroid_X = int(longest_contour_list[j].Centroid[0])
            Temp_Centroid_Y = int(longest_contour_list[j].Centroid[1])

            if (Main_Centroid_X-Centroid_acceptable_distance < Temp_Centroid_X < Main_Centroid_X+Centroid_acceptable_distance) and (Main_Centroid_Y-Centroid_acceptable_distance < Temp_Centroid_Y < Main_Centroid_Y+Centroid_acceptable_distance):
                resulting_contour = np.append(longest_contour_list[i].Contour,longest_contour_list[j].Contour,axis=0)
                longest_contour_list[i] = Contour(resulting_contour)
                longest_contour_list[i].fitEllipse()

    longest_contour_list.sort(key=operator.attrgetter('Area'),reverse=True)

    contour_draw_list = list()
    ellipse_draw_list = list()

    Contour_number_drawing = min(Slider_list.Slider_list[11].value(),len(longest_contour_list))

    for i in range(Contour_number_drawing):
        try:
            # print(canny_contour_list[i].Contour)
            contour_draw_list.append(longest_contour_list[i].Contour)
            ellipse = cv2.fitEllipse(longest_contour_list[i].Contour)
            ellipse_center = (int(ellipse[0][0]),int(ellipse[0][1]))
            Img_with_only_pupil = cv2.circle(Img_with_only_pupil, ellipse_center , 5, (255, 255, 255), 2)
            Img_with_only_pupil = cv2.ellipse(Img_with_only_pupil,ellipse,(0,255,0),2)
        except:
            pass

    # print(canny_contour_list[0].Contour)
    # print(canny_contour_list[0].Contour.shape)

    # resulting_contour = np.append(canny_contour_list[0].Contour,canny_contour_list[3].Contour,axis=0)
    # # print(resulting_contour.shape)
    # ellipse = cv2.fitEllipse(resulting_contour)

    # Img_with_only_pupil = cv2.ellipse(Img_with_only_pupil, ellipse, (0, 255, 0), 2)

    cv2.drawContours(Img_with_canny_contours, contour_draw_list, contourIdx=-1, thickness=1, color=(255, 255, 255))

    # cv2.drawContours(Img_with_canny_contours, hull_canny, contourIdx=-1, thickness=1, color=(255, 255, 255))

    Pupil_kernel = np.ones((Slider_list.Slider_list[2].value(),Slider_list.Slider_list[2].value()),np.uint8)

    # erosion = cv2.erode(Pupil_gaussian_threshold, Pupil_kernel, iterations=1)
    # dilation = cv2.dilate(Pupil_gaussian_threshold, Pupil_kernel, iterations=1)

    h1 = np.hstack((grayscaled,edges_canny))
    h2 = np.hstack((Img_with_only_pupil,Img_with_canny_contours))
    res = np.vstack((h1,h2))
    cv2.imshow('image',res)
    # cv2.imshow('Binary',Pupil_binary_threshold)


    key = cv2.waitKey(1)

    Timer_1.Update_elapsed_time(Print_elapsed_time=True,Precise_time=True)
    if key == 27:
        break
cv2.destroyAllWindows()
sys.exit(app.exec_())

# dst = cv2.inpaint(img, threshold, 3, cv2.INPAINT_TELEA)
# retval, threshold = cv2.threshold(grayscaled, Slider_list.Slider_list[3].value(), Slider_list.Slider_list[2].value(), cv2.THRESH_BINARY)

# blur_size = ((Slider_list.Slider_list[4].value() * 2 + 3), (Slider_list.Slider_list[3].value() * 2 + 3))
# blur = cv2.GaussianBlur(Contrast_corrected1, blur_size, 0)
# sharp = Contrast_corrected1 + (Contrast_corrected1 - blur) * (Slider_list.Slider_list[2].value())

# gradient = cv2.morphologyEx(Pupil_gaussian_threshold, cv2.MORPH_GRADIENT, Pupil_kernel)
# tophat = cv2.morphologyEx(Pupil_gaussian_threshold, cv2.MORPH_TOPHAT, Pupil_kernel)
# blackhat = cv2.morphologyEx(Pupil_gaussian_threshold, cv2.MORPH_BLACKHAT, Pupil_kernel)
# Pupil_opening = cv2.morphologyEx(Pupil_gaussian_threshold, cv2.MORPH_OPEN, Pupil_kernel, iterations=Slider_list.Slider_list[3].value() + 1)