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



videoname = '4_19_human_demo_origin'
path="D:/throat swab/video/test_video/"+videoname+"orign.mp4"
cap,retu=find_camera().open_camera(cam_n=None,path=path)
# Ret=0
# print(retu)

file_path="D:/throat swab/video/test_video/"
file1=videoname+'re_test.mp4' 
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # mp4
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(file_path+file1,fourcc,25,size)

cx=640
de=detect(thresh_draw=True,contour_draw=True,circle_draw=True,n_cl=3)



def main_fun(de):
    in_position=[640,150]
    i=0 
    test_num=0
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
    





