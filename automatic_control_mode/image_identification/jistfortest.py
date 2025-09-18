import serial
import serial.tools.list_ports
import time
import cv2
import math

ser = serial.Serial(com='COM5',bps=9600,timeout=0.5)



def Recive_data():
    # 循环接收数据，此为死循环，可用线程实现
    data='no data'
    try:
        data = ser.readline()#方式二print("接收ascii数据：", data)
        data = data.strip()
        # data = data.decode('utf-8','ignore')   
        time.sleep(0.05)

    except Exception as e:
        print("异常报错：",e)
        data=None
    return data

print(Recive_data())   