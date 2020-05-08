import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('Eye_00001.png',0)
# create a CLAHE object (Arguments are optional).
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)

res = np.hstack((img,cl1)) #stacking images side-by-side

cv2.imshow('clahe_2.jpg',res)
