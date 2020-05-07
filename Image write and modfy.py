import cv2
import numpy as np
import os

Raw_image_dir = r'C:\Users\minu\PycharmProjects\eye tracker test\Dataset\Raw images'
os.chdir(Raw_image_dir)
files = os.listdir(Raw_image_dir)

for file in files:
    print(file)
    os.chdir(Raw_image_dir)
    img = cv2.imread(file)
    ##retval, binary = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gauss = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 1)
    ##cv2.imshow('original',img)
    ##cv2.imshow('binary',binary)
    ##cv2.imshow('gauss',gauss)
    Gauss_image_dir = r'C:\Users\minu\PycharmProjects\eye tracker test\Dataset\Gaussian images'
    os.chdir(Gauss_image_dir)
    filename = file.replace('png','_Gauss.png')
    cv2.imwrite(file,gauss)


cv2.waitKey(0)
cv2.destroyAllWindows()
