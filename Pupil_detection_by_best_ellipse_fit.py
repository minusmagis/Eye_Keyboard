
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

#We set the averaging of the frames that determines the current ellipse position
Frame_averages = 1

# This function takes two ellipses and averages them weightedly
def Average_ellipse(Ellipse_1,Ellipse_2,weight = (1,1)):
    avg_center_x = ((Ellipse_1[0][0] * weight[0])+(Ellipse_2[0][0] * weight[1])) / (weight[0]+weight[1])
    avg_center_y = ((Ellipse_1[0][1] * weight[0])+(Ellipse_2[0][1] * weight[1])) / (weight[0]+weight[1])
    avg_size_x = ((Ellipse_1[1][0] * weight[0])+(Ellipse_2[1][0] * weight[1])) / (weight[0]+weight[1])
    avg_size_y = ((Ellipse_1[1][1] * weight[0])+(Ellipse_2[1][1] * weight[1])) / (weight[0]+weight[1])
    avg_angle = ((Ellipse_1[2] * weight[0])+(Ellipse_2[2] * weight[1])) / (weight[0]+weight[1])
    return ((avg_center_x,avg_center_y),(avg_size_x,avg_size_y),avg_angle)

def Ellipse_area(ellipse):
    return(ellipse[1][0] * ellipse[1][1] * 3.1415926535)

class Avg_Ellipse:
    def __init__(self,ellipse):
        self.averages = 0
        self.ellipse = ellipse
        self.area = ellipse[1][0] * ellipse[1][1] * 3.141592653

class Contour:
    def __init__(self,Contour):
        self.Contour = Contour
        self.Hull = cv2.convexHull(self.Contour, False)
        self.Area = cv2.contourArea(self.Hull)
        self.Arc_length = cv2.arcLength(self.Contour,False)
        self.Centroid = 0,0
        self.Size = 0,0
        self.ellipse = 0
        self.Fit_error = 0          # Fit_error, the smaller the better
        self.Full_error = 0         # It combines the fit error with the fact that the contour is large selecting only those who are large and also have good fits

    def fitEllipse(self):
        self.ellipse = cv2.fitEllipse(self.Contour)
        self.Centroid = (int(self.ellipse[0][0]),int(self.ellipse[0][1]))
        self.Angle = (int(self.ellipse[2])/ 180) * 3.1415926535
        self.Size = (int(self.ellipse[1][0]),int(self.ellipse[1][1]))

        X = np.squeeze(self.Contour[:, :, [0]])
        Y = np.squeeze(self.Contour[:, :, [1]])

        for index,contour_point in enumerate(X):
            posx = (X[index] - self.Centroid[0]) * math.cos(-self.Angle) - (Y[index]- self.Centroid[1]) * math.sin(-self.Angle)
            posy = (X[index] - self.Centroid[0]) * math.sin(-self.Angle) + (Y[index]- self.Centroid[1]) * math.cos(-self.Angle)
            self.Fit_error += abs( (posx / self.Size[0]) * (posx / self.Size[0]) + (posy / self.Size[1]) * (posy / self.Size[1]) - 0.25)

        self.Full_error = len(X) / self.Fit_error




# This is used to initiate the GUI
app = QApplication(sys.argv)

# We define the sliders we want to calibrate the software with the Slider class created in the Slider.py script
blockSize_slider = Slider.Slider('Block Size',1,800,Starting_value=212)                                                # 0
Substract_Constant = Slider.Slider('Substract Constant',-2,800,Starting_value=23)                                    # 1
Pupil_Kernel = Slider.Slider('Pupil_Kernel',1,50,Starting_value=1)                                                  # 2
Binary_threshold_low = Slider.Slider('Binary_threshold_low',0,255,Starting_value=0)                                 # 3
Binary_threshold_high = Slider.Slider('Binary_threshold_low',0,255,Starting_value=0)                                # 4
Pupil_opening_iterations = Slider.Slider('Pupil_opening_iterations',0,20,Starting_value=0)                          # 5
Canny_threshold_1 = Slider.Slider('Canny_threshold_1',0,300,Starting_value=27)                                # 6
Canny_threshold_2 = Slider.Slider('Canny_threshold_2',0,300,Starting_value=17)                                # 7
post_glare_blur_size =  Slider.Slider('post_glare_blur_size',0,50,Starting_value=1)                                # 8
contour_number_analyzing_selection =  Slider.Slider('contour_number_analyzing_selection',0,50,Starting_value=20)                                # 9
contour_ellipse_centroid_distance =  Slider.Slider('contour_ellipse_centroid_distance',0,300,Starting_value=20)                                # 10
contour_number_drawing_selection =  Slider.Slider('contour_number_drawing_selection',0,50,Starting_value=20)                                # 11
Full_error_threshold =  Slider.Slider('Full_error_threshold',0,50,Starting_value=1)                                # 11


# Now we define the main window with all the desired sliders as a list
Slider_list = Slider.Slider_window([blockSize_slider,Substract_Constant,Pupil_Kernel,Pupil_opening_iterations,Binary_threshold_low,Binary_threshold_high,Canny_threshold_1,Canny_threshold_2,post_glare_blur_size,contour_number_analyzing_selection,contour_ellipse_centroid_distance,contour_number_drawing_selection,Full_error_threshold])

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

prev_contour_count = 0
ellipse_average_list = list()
prev_contour_list = list()

# We loop infinitely through the camera feed or through the same image to adjust the computation parameters
while True:
    # Timer_1 = sf.Timer()                      # We start a timer to see the elapsed time

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

    Pupil_gaussian_threshold = cv2.adaptiveThreshold(glare_Corrected_gaussian_blured, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,  Slider_list.Slider_list[0].value()*2+1,  Slider_list.Slider_list[1].value())

    edges_canny = cv2.Canny(glare_Corrected_gaussian_blured, Slider_list.Slider_list[6].value(), Slider_list.Slider_list[7].value(),)

    contours_canny, hierarchy = cv2.findContours(edges_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    Img_with_canny_contours = copy.copy(glare_Corrected_gaussian_blured)
    Img_with_only_pupil = copy.copy(glare_Corrected_gaussian_blured)

    canny_contour_list = list()
    # print(len(contours))

    for contour in contours_canny:
        canny_contour_list.append(Contour(contour))

    canny_contour_list.sort(key=operator.attrgetter('Arc_length'),reverse=True)

    contour_analyze_count = Slider_list.Slider_list[9].value()
    longest_contour_list = list()

    for i in range(contour_analyze_count):
        try:
            canny_contour_list[i].fitEllipse()
            longest_contour_list.append(canny_contour_list[i])
        except:
            pass

    Centroid_acceptable_distance = Slider_list.Slider_list[10].value()

    longest_contour_list.sort(key=operator.attrgetter('Full_error'),reverse=True)
    ellipse_average_list.sort(key=operator.attrgetter('area'),reverse=True)

    draw_contour_list = list()

    for i in range(len(longest_contour_list)):
        Curr_Centroid_X = int(longest_contour_list[i].Centroid[0])
        Curr_Centroid_Y = int(longest_contour_list[i].Centroid[1])
        # print('-----------------')
        # print(Main_Centroid_X)
        # print(Main_Centroid_Y)
        for j in range(len(prev_contour_list)):
            Prev_Centroid_X = int(prev_contour_list[j].Centroid[0])
            Prev_Centroid_Y = int(prev_contour_list[j].Centroid[1])
            # print(Prev_Centroid_X)
            # print(Prev_Centroid_Y)

            if (Prev_Centroid_X-Centroid_acceptable_distance < Curr_Centroid_X < Prev_Centroid_X+Centroid_acceptable_distance) and (Prev_Centroid_Y-Centroid_acceptable_distance < Curr_Centroid_Y < Prev_Centroid_Y+Centroid_acceptable_distance):

                for k in range(len(ellipse_average_list)):
                    Average_Centroid_X = int(ellipse_average_list[k].ellipse[0][0])
                    Average_Centroid_Y = int(ellipse_average_list[k].ellipse[0][1])
                    if (Average_Centroid_X - Centroid_acceptable_distance < Curr_Centroid_X < Average_Centroid_X + Centroid_acceptable_distance) and (Average_Centroid_Y - Centroid_acceptable_distance < Curr_Centroid_Y < Average_Centroid_Y + Centroid_acceptable_distance):
                        prev_avg_count = ellipse_average_list[k].averages
                        ellipse_average_list[k] = Avg_Ellipse(Average_ellipse(ellipse_average_list[k].ellipse,longest_contour_list[i].ellipse,(Frame_averages-1,1)))
                        ellipse_average_list[k].averages = min(prev_avg_count+2,Frame_averages)
                        draw_contour_list.append(longest_contour_list[i])
                        break
                    else:
                        ellipse_average_list.append(Avg_Ellipse(longest_contour_list[i].ellipse))
                        ellipse_average_list[-1].averages = 2

                if len(ellipse_average_list) == 0:
                    ellipse_average_list.append(Avg_Ellipse(longest_contour_list[i].ellipse))


            break


    for index,ellipse in enumerate(ellipse_average_list):
        # print(ellipse.averages)
        ellipse.averages -=1
        if ellipse.averages <=0:
            ellipse_average_list.pop(index)

    print(len(ellipse_average_list))

    contour_draw_list = list()
    ellipse_draw_list = list()

    Contour_number_drawing = min(Slider_list.Slider_list[11].value(),len(longest_contour_list))

    for i in range(Contour_number_drawing):
        # if prev_contour_count != Contour_number_drawing or Camera:
        #     print('Fit error of the ' +str(i)+' contour: ' +str(longest_contour_list[i].Fit_error)+'   Full error of the ' +str(i)+' contour: ' +str(longest_contour_list[i].Full_error))
        try:
            contour_draw_list.append(longest_contour_list[i].Contour)
            ellipse = ellipse_average_list[i].ellipse
            ellipse_center = (int(ellipse[0][0]),int(ellipse[0][1]))
            Img_with_only_pupil = cv2.circle(Img_with_only_pupil, ellipse_center , 5, (255, 255, 255), 2)
            Img_with_only_pupil = cv2.ellipse(Img_with_only_pupil,ellipse,(0,255,0),2)
        except:
            pass

    # if prev_contour_count != Contour_number_drawing or Camera:
    #     print('-------------------------------------------')
    # print(canny_contour_list[0].Contour)
    # print(canny_contour_list[0].Contour.shape)

    # resulting_contour = np.append(canny_contour_list[0].Contour,canny_contour_list[3].Contour,axis=0)
    # # print(resulting_contour.shape)
    # ellipse = cv2.fitEllipse(resulting_contour)

    # Img_with_only_pupil = cv2.ellipse(Img_with_only_pupil, ellipse, (0, 255, 0), 2)

    cv2.drawContours(Img_with_canny_contours, contour_draw_list, contourIdx=-1, thickness=1, color=(255, 255, 255))

    h1 = np.hstack((grayscaled,edges_canny))
    h2 = np.hstack((Img_with_only_pupil,Img_with_canny_contours))
    res = np.vstack((h1,h2))
    cv2.imshow('image',res)
    # cv2.imshow('Binary',Pupil_binary_threshold)

    prev_contour_count = Contour_number_drawing
    prev_contour_list = longest_contour_list

    key = cv2.waitKey(1)

    # Timer_1.Update_elapsed_time(Print_elapsed_time=True,Precise_time=True)
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