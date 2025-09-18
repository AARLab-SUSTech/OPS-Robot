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




camera_number=1
cap,retu=find_camera().open_camera(cam_n=camera_number)

videoname = '4_19_human_demo_origin'
# path="D:/throat swab/video/test_video/"+videoname+"orign.mp4"
# cap,retu=find_camera().open_camera(cam_n=None,path=path)
# Ret=0
# print(retu)

file_path="D:/throat swab/video/test_video/"
file1=videoname+'test.mp4' 
file2=videoname+'orign.mp4' 
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # mp4
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(file_path+file1,fourcc,25,size)
out_or = cv2.VideoWriter(file_path+file2,fourcc,25,size)

cx=640
de=detect(thresh_draw=True,contour_draw=True,circle_draw=True,n_cl=3)
opera=operation(port="COM3",baudrate=115200, )
Ret=opera.connecting()
ready_to_sampling = False
# Ret=1

global Force_list
force_list=np.zeros((1,650))

def add_force(opera,image0,item):
    a=0
    num=opera.getfeedback()
    time.sleep(0.001)
    if num!="":
        num=int(num)
        if num==1234:
            a=1
    else:
        num=0
    force_list[0,item]=num
    return a


def end_sig():
    a=0
    num=opera.getfeedback()
    if num!="":
        if int(num)==1234:
            a=1
    return a

def main_fun(Ret,de,ready_to_sampling,):
    in_position=[640,150]
    i=0 
    test_num=0
    getdata=0
    is_end=0
    while Ret:
        ret,image = cap.read() 
        out_or.write(image)
        if ret == True:
            i+=1
            # print('item = ',i)
            if i%2 ==0:
                try:
                    start = time.time()
                    # boolean = de.weather_swab(image, thr=80)
                    # print(boolean)
                    image, cx, cy = de.find_xy(image)   
                    end = time.time()
                    if ready_to_sampling==False:
                        print("time:",int((end-start)*1000))
                        print("position",cx,"//",cy)
                        
                        if (cx<740 and cx>500 and cy<250 and cy>50):
                            test_num=test_num+1
                            if test_num>=10:
                                ready_to_sampling=True
                                in_position=[cx,cy]
                                print("center in position is://",in_position,"//")
                                opera.send_run(position=in_position)
                                getdata=1
                        else:
                            test_num=0

                except Exception as e:
                    print('NO detected!',e)
                
                if getdata:
                    is_end=end_sig()
                    # print(is_end)
                cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
                cv2.imshow('image',image) 
                cv2.waitKey(1)
                out.write(image)
                # cv2.imwrite(path+'picture/'+str(i)+'.jpg',image)
                
            
            if i>500 or is_end==1:
                print(i)
                # print(is_end)
                print("finished")
                # operation.run_mechine(position=center)
                break

        else:
            print('item:',i)
            break
    return in_position


# def open_app(app_dir =r'C:\Users\22135\Desktop\相机'):
#   os.startfile(app_dir)



if __name__ == "__main__":

    center=main_fun(Ret,de,ready_to_sampling,)
    cap.release()
    # np.savetxt("force_list_"+videoname+".txt",force_list)
    # cv2.destroyAllWindows()
    # open_app(r'C:\Users\22135\Desktop\相机')
    # sampling(opera,True,center)
    





