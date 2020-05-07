import cv2
import numpy as np
import os
import tkinter
import TXT_importer as txtimp

Raw_image_dir = r'C:\Users\minu\PycharmProjects\eye tracker test\Dataset\Raw images 2'
Dataset_values_filename = r'C:\Users\minu\PycharmProjects\eye tracker test\Dataset\Dataset Files\Center and Ellipse Values Raw dataset 2.txt'


os.chdir(Raw_image_dir)
files = os.listdir(Raw_image_dir)

xy_master_previous = [0,0]
xy_master = [0,0]

def mouse_drawing(event, x, y, flags, params):
    global xy_master
    if event == cv2.EVENT_LBUTTONUP:
        xy_master = [x,y]



root = tkinter.Tk()

# scale = tkinter.Scale(orient='horizontal', from_=2, to=254, resolution=2,length= 1000, label = 'bilateral blur')
scale2 = tkinter.Scale(orient='horizontal', from_=2, to=1201,  resolution=2,length= 1000,label = 'block size')
scale3 = tkinter.Scale(orient='horizontal', from_=-2, to=100,  resolution=0.05,length= 1000,label = 'Constant Substracted')
scale4 = tkinter.Scale(orient='horizontal', from_=3, to=700, resolution=1,length= 1000, label = 'Manual point placement x')
scale5 = tkinter.Scale(orient='horizontal', from_=3, to=700, resolution=1,length= 1000, label = 'Manual point placement y')
Manual = tkinter.IntVar()
c = tkinter.Checkbutton(root, text="Manual Mode", variable=Manual)

c.pack()
# scale.pack()
scale2.pack()
scale3.pack()
scale4.pack()
scale5.pack()

scale = 0
# scale2 = 756
# scale3 = 22.55
# scale4 = 3
# scale5 = 3

Dataset_values = [[]]
Dataset_values_ind = []

Analized_files = txtimp.import_txt_to_string_list(Dataset_values_filename)
Analized_filenames = txtimp.import_txt_to_string_list_one_col_only(Dataset_values_filename)
#print(Analized_filenames)

for file in files:
    First_append = True
    ellipse_manual_points = [[]]
    if file in Analized_filenames:
        pass
        #print('Already analized: '+file+'\n')
    else:
        while True:
            root.update_idletasks()
            root.update()
            os.chdir(Raw_image_dir)
            #print(scale.get())
            img = cv2.imread(file)
            flipBoth = cv2.flip(img, -1)
            ##retval, binary = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
            grayscaled = cv2.cvtColor(flipBoth,cv2.COLOR_BGR2GRAY)
            gauss = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, int(scale2.get()+1), scale3.get())
            #bilateral = cv2.bilateralFilter(gauss, int(scale.get()+1),1,1)
            edges = cv2.Canny(gauss, 3, 3)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if Manual.get():
                cv2.setMouseCallback('edges', mouse_drawing)
                if xy_master != xy_master_previous:
                    if First_append:
                        ellipse_manual_points = [xy_master]
                        First_append = False
                    else:
                        ellipse_manual_points.append(xy_master)
                    print(ellipse_manual_points)
                    ellipse_manual_points_array = np.array([np.array(xi) for xi in ellipse_manual_points])
                    print(ellipse_manual_points_array)
                    xy_master_previous = xy_master
                cv2.drawMarker(flipBoth,(int(scale4.get()),int(scale5.get())),(255,255,255))
                cv2.drawMarker(gauss,(int(scale4.get()),int(scale5.get())),(255,255,255))
            if Manual.get() and len(ellipse_manual_points) >=5:
                ellipse = cv2.fitEllipse(ellipse_manual_points_array)
                cv2.ellipse(flipBoth, ellipse, (0, 255, 0), thickness=1)
                cv2.circle(flipBoth, (int(ellipse[0][0]), int(ellipse[0][1])), 5, (0, 0, 255), 4)
                cv2.ellipse(gauss, ellipse, (0, 255, 0), thickness=1)
                cv2.circle(gauss, (int(ellipse[0][0]), int(ellipse[0][1])), 5, (0, 0, 255), 4)
                for point in ellipse_manual_points:
                    cv2.circle(flipBoth,(point[0],point[1]),1,(0,0,255),1)
            else:
                hull = []
                ellipse = []
                area = []
                current_contour_count = len(contours)
                for i in range(len(contours)):
                    hull.append(cv2.convexHull(contours[i], False))
                    area.append(cv2.contourArea(hull[i]))
                last_contour_count = current_contour_count
                if len(area) >= 1:
                    biggest_contour_0 = area.index(max(area))
                    area[biggest_contour_0] = 0
                    if len(contours[biggest_contour_0]) > 6:
                        ellipse = cv2.fitEllipse(contours[biggest_contour_0])
                        cv2.ellipse(flipBoth, ellipse, (0, 255, 0), thickness=1)
                        cv2.circle(flipBoth, (int(ellipse[0][0]), int(ellipse[0][1])), 5, (0, 0, 255), 4)
                        cv2.drawContours(flipBoth,contours,contourIdx= biggest_contour_0,thickness=1,color = (255,255,255))
            #print(len(contours))
            #cv2.line(flipBoth,(262,194),(106, 129),(255,0,0),1)
            ##cv2.imshow('original',img)
            ##cv2.imshow('binary',binary)
            #cv2.imshow('medial',bilateral)
            #cv2.resizeWindow(file, 6000, 6000)
            cv2.imshow('edges', edges)
            cv2.imshow('gauss',gauss)
            cv2.imshow(file, flipBoth)
            Gauss_image_dir = r'C:\Users\minu\PycharmProjects\eye tracker test\Dataset\Gaussian images'
            os.chdir(Gauss_image_dir)
            #filename = file.replace('png','_Gauss.png')
            #cv2.imwrite(file,gauss)
            key = cv2.waitKey(1)

            if key == 97:
                Dataset_values_ind = [file,ellipse]
                Dataset_values.append([file,ellipse])
                #print(Dataset_values)
                TXT_file = open(Dataset_values_filename,'a')
                TXT_file.write(str(Dataset_values_ind)+'\n')
                TXT_file.close()
                cv2.destroyAllWindows()
                break
            elif key == 98:
                #print(Dataset_values)
                TXT_file = open(Dataset_values_filename,'a')
                TXT_file.write("['"+ str(file) + "', Blink]\n")
                TXT_file.close()
                cv2.destroyAllWindows()
                break
            elif key == 114:
                cv2.destroyAllWindows()
                break
            # elif key == 110:
            #     if First_append:
            #         ellipse_manual_points = [[int(scale4.get()),int(scale5.get())]]
            #         First_append = False
            #     else:
            #         ellipse_manual_points.append([int(scale4.get()),int(scale5.get())])
            #     ellipse_manual_points_array = np.array([np.array(xi) for xi in ellipse_manual_points])
            #     print(ellipse_manual_points_array)


#print(Dataset_values)



cv2.destroyAllWindows()