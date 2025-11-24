import serial
import serial.tools.list_ports
import time
import cv2
import math

ser = serial.Serial(com='COM5',bps=9600,timeout=0.5)



def Recive_data():
    
    data='no data'
    try:
        data = ser.readline()
        data = data.strip()
        # data = data.decode('utf-8','ignore')   
        time.sleep(0.05)

    except Exception as e:
        print("异常报错：",e)
        data=None
    return data

print(Recive_data())   