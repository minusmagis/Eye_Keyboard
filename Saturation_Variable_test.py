
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
import Slider
import sys
import cv2

# This is used to initiate the GUI
app = QApplication(sys.argv)

# We define the sliders we want to calibrate the software with the Slider class created in the Slider.py script
Width_slider = Slider.Slider('Width',1,1980,Starting_value=640)                                                # 0
Height_Slider = Slider.Slider('Height', 1, 1080, Starting_value=480)                                    # 1
Brightness_Slider = Slider.Slider('Brightness',0,255,Starting_value=249)                                                  # 2
Contrast_Slider = Slider.Slider('Contrast',0,255,Starting_value=255)                                 # 3
Saturation_Slider = Slider.Slider('Saturation',0,255,Starting_value=0)                                # 4
Hue_Slider = Slider.Slider('Hue',0,20,Starting_value=20)                          # 5
Gain_Slider = Slider.Slider('Gain',0,127,Starting_value=78)                                # 6
Exposure_Slider = Slider.Slider('Exposure',-7,-1,Starting_value=-7)                                # 7
White_Balance_Slider =  Slider.Slider('White_Balance',4000,7000,Starting_value=5000)                                # 8
Focus_Slider =  Slider.Slider('Focus',0,255,Starting_value=125,Step_size=5)                                # 9

# Now we define the main window with all the desired sliders as a list
Slider_list = Slider.Slider_window([Width_slider, Height_Slider, Brightness_Slider, Contrast_Slider, Saturation_Slider, Hue_Slider, Gain_Slider, Exposure_Slider, White_Balance_Slider, Focus_Slider])

# We assign the camera feed to a variable to treat it and use it afterwards

cap = cv2.VideoCapture(1)
# cap.set(3 , 1280 ) # width
# cap.set(4 , 720  ) # height

# We show the Slider window
Slider_list.show()

while True:

    cap.set(10, Slider_list.Slider_list[2].value())  # brightness     min: 0   , max: 255 , increment:1
    cap.set(11, Slider_list.Slider_list[3].value())  # contrast       min: 0   , max: 255 , increment:1
    cap.set(12, Slider_list.Slider_list[4].value())  # saturation     min: 0   , max: 255 , increment:1
    cap.set(13, Slider_list.Slider_list[5].value())  # hue
    cap.set(14, Slider_list.Slider_list[6].value())  # gain           min: 0   , max: 127 , increment:1
    cap.set(15, Slider_list.Slider_list[7].value())  # exposure       min: -7  , max: -1  , increment:1
    cap.set(17, Slider_list.Slider_list[8].value())  # white_balance  min: 4000, max: 7000, increment:1
    cap.set(28, Slider_list.Slider_list[9].value())  # focus          min: 0   , max: 255 , increment:5
    # We take a frame from the feed and process it. First we grayscale it so that it is easier to process
    _, frame = cap.read()

    cv2.imshow('image',frame)
    key = cv2.waitKey(1)

    if key == 27:
        break



cap.release()
cv2.destroyAllWindows()