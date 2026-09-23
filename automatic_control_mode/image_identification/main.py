import threading
import time
from detect import detect
import numpy as np
import cv2 as cv2
from communication import Communication as com
from communication import find_camera
from move import operation
from multiprocessing import Process
import os
import time

camera_number = 1
cap, retu = find_camera().open_camera(cam_n=camera_number)

cx = 640
de = detect(thresh_draw=True, contour_draw=True, circle_draw=True, n_cl=3)
opera = operation(port="COM3", baudrate=115200, )
Ret = opera.connecting()
ready_to_sampling = False
# Ret=1

global Force_list
force_list = np.zeros((1, 650))

def add_force(opera, image0, item):
    a = 0
    num = opera.getfeedback()
    time.sleep(0.001)
    if num != "":
        num = int(num)
        if num == 1234:
            a = 1
    else:
        num = 0
    force_list[0, item] = num
    return a


def end_sig():
    a = 0
    num = opera.getfeedback()
    # The lower computer may answer with non-numeric text (e.g. "ok"),
    # so only convert once the payload is actually a number.
    if num is not None and num.strip().isdigit():
        if int(num) == 1234:
            a = 1
    return a


def main_fun(Ret, de, ready_to_sampling, ):

    in_position = [640, 150]
    i = 0
    test_num = 0
    getdata = 0
    is_end = 0
    px_t1 = 0
    py_t1 = 0
    px_t2 = 0
    py_t2 = 0
    box_initialized = False

    while Ret:
        ret, image = cap.read()
        if ret == True:
            i += 1
            # print('item = ',i)
            if i % 2 == 0:
                try:
                    start = time.time()
                    # boolean = de.weather_swab(image, thr=80)
                    # print(boolean)
                    image, cx, cy = de.find_xy(image)
                    end = time.time()
                    if ready_to_sampling == False:
                        print("time:", int((end - start) * 1000))
                        print("position", cx, "//", cy)

                        if not box_initialized:

                            px_t1 = cx - target_length / 2
                            py_t1 = cy - target_length / 2
                            px_t2 = cx + target_length / 2
                            py_t2 = cy + target_length / 2
                            box_initialized = True

                        if (cx <= px_t2 and cx >= px_t1 and cy <= py_t2 and cy >= py_t1):
                            test_num = test_num + 1
                            # print("test num is://", test_num)
                            if test_num >= 10:
                                ready_to_sampling = True
                                in_position = [cx, cy]
                                print("center in position is://", in_position, "//")
                                opera.send_run(position=in_position)
                                getdata = 1
                        else:
                            test_num = 0

                except Exception as e:
                    print('NO detected!', e)

                if getdata:
                    is_end = end_sig()
                    # print(is_end)
                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                cv2.imshow('image', image)
                cv2.waitKey(1)
                # cv2.imwrite(path+'picture/'+str(i)+'.jpg',image)

            if i > 500 or is_end == 1:
                print(i)
                # print(is_end)
                print("finished")
                operation.run_mechine(position=in_position)
                break

        else:
            print('item:', i)
            break
    return in_position

if __name__ == "__main__":
    center = main_fun(Ret, de, ready_to_sampling, )
    cap.release()
    # np.savetxt("force_list_"+videoname+".txt",force_list)
    # cv2.destroyAllWindows()
    # open_app(r'C:\Users\22135\Desktop\相机')
    # sampling(opera,True,center)
