import threading
import time
from detect import detect
import numpy as np
import cv2 as cv2
from communication import Communication as com
from communication import find_camera
from move import operation
from multiprocessing import Process
import os, time
# import Matplotlab as plt


de=detect(thresh_draw=True,contour_draw=True,circle_draw=True,n_cl=3)



def main_fun(de):
   
    while 1:
        ret,image = cap.read() 
        if ret == True:
            i+=1
            # print('item = ',i)
            if i%1 ==0:
                try:
                    start = time.time()
                    # boolean = de.weather_swab(image, thr=80)
                    # print(boolean)
                    image, cx, cy = de.find_xy(image)   
                    end = time.time()

                except Exception as e:
                    print('NO detected!',e)
                
                cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
                cv2.imshow('image',image) 
                cv2.waitKey(1)
                out.write(image)
                # cv2.imwrite(path+'picture/'+str(i)+'.jpg',image)

        else:
            print('item:',i)
            break
    return in_position




if __name__ == "__main__":

    center=main_fun(de)
    cap.release()
    # np.savetxt("force_list_"+videoname+"or.txt",force_list)
    # cv2.destroyAllWindows()
    # open_app(r'C:\Users\22135\Desktop\相机')
    # sampling(opera,True,center)
    





