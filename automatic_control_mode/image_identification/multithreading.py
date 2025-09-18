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
from copy import deepcopy

thread_lock = threading.Lock()
thread_exit = False
test_num=0




class myThread(threading.Thread):
    def __init__(self, camera_id=1, img_height=720, img_width=1280):
        super(myThread, self).__init__()
        self.camera_id = camera_id
        self.img_height = img_height
        self.img_width = img_width
        self.frame = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    def get_frame(self):
        return deepcopy(self.frame)

    def run(self):
        global thread_exit
        global test_num
        # de=detect(thresh_draw=False,contour_draw=True,circle_draw=True,n_cl=3)
        # opera=operation(port="COM4",baudrate=115200, )
        # cap = cv2.VideoCapture(self.camera_id)
        cap,retu=find_camera().open_camera(cam_n=self.camera_id)
        while not thread_exit:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (self.img_width, self.img_height))
                frame, cx, cy = de.find_xy(frame) 
                print("position",cx,"//",cy) 
                if (cx<740 and cx>500 and cy<250 and cy>50):
                    test_num=test_num+1
                    print(test_num)
                    if test_num>=1:
                        in_position=[cx,cy]
                        print("center in position is://",in_position,"//")
                        opera.run_mechine(position=in_position)
                        # if open:
                        #     break
                        #     # break
                else:
                    test_num=0
                thread_lock.acquire()
                self.frame = frame
                thread_lock.release()
            else:
                thread_exit = True
        cap.release()

def main():
    global thread_exit
    camera_id = 0
    img_height = 720
    img_width = 1280
    thread = myThread(camera_id, img_height, img_width)
    thread.start()

    while not thread_exit:
        thread_lock.acquire()
        frame = thread.get_frame()

        thread_lock.release()
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL) 
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            thread_exit = True
    thread.join()







if __name__ == "__main__":
    de=detect(thresh_draw=False,contour_draw=True,circle_draw=True,n_cl=3)
    opera=operation(port="COM4",baudrate=115200, )
    Ret=opera.connecting()
    main()


