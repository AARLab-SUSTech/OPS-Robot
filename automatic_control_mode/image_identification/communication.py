import serial
import serial.tools.list_ports
import time
import cv2
import math


class Communication():

    # Initialization
    def __init__(self, com='COM4', bps=9600, timeout=0.05):
        self.port = com
        self.bps = bps
        self.timeout = timeout
        global Ret
        Ret = False
        try:
            # Open the serial port and get the serial object
            self.ser = serial.Serial(self.port, self.bps, timeout=self.timeout)
            # Check whether it was opened successfully
            if (self.ser.is_open):
                Ret = True
        except Exception as e:
            print("---exception--- serial not open:", e)

    def if_Open_Ser(self):
        return_sig = "",
        Ret = self.engin1.Open_Engine()
        if Ret == True:
            self.engin1.send("SSS")
            return_sig = self.engin1.Recive_data()
            time.sleep(0.01)

        return return_sig

    def connect(self):
        Ret_sig = ""
        ret = 0
        while(1):
            if Ret == True:
                self.send("ready")
                print("sended ready")
                Ret_sig = self.Recive_data()
                time.sleep(0.01)
            else:
                print("Please connect the Bluetooth...")

            if Ret_sig == "4":
                ret = 1
                print("received:", Ret_sig)
                print("connected...")
                break
            else:
                print("Waiting connection feedback......")
                print(Ret_sig)
            time.sleep(1)
        return ret

    def Open_Engine(self):
        return Ret

    # Close the serial port
    def Close_Engine(self):
        self.ser.close()
        print(self.ser.is_open)  # Check whether the serial port is open

    def send(self, data):
        try:
            self.ser.write(data.encode('utf-8'))
        except Exception as e:
            print("exception, no send:", e)

    def Recive_data(self,):
        # Receive data in a loop; this is an infinite loop and can be run in a thread
        data = 'no data'
        data = self.ser.readline()  # option 2: print("received ascii data:", data)
        data = data.strip()
        data = data.decode('utf-8', 'ignore')
        time.sleep(0.001)
        return data

    # def Recive_data(self,):
    #     # Receive data in a loop; this is an infinite loop and can be run in a thread
    #     data='no data'
    #     try:
    #         data = self.ser.readline()# option 2: print("received ascii data:", data)
    #         data = data.strip()
    #         data = data.decode('utf-8','ignore')
    #         time.sleep(0.002)

    #     except Exception as e:
    #         print("exception, no received data!:",e)
    #         data=None
    #     return data

    def pixel_to_angle(self, xy, z):
        pixel_x = xy[0]
        pixel_y = xy[1]
        pixel_center = [640, 150]
        pixel_ratio = 0.05
        z0 = 190.5
        # Z0=175
        x_0 = 510
        y_0 = 665
        print("xy", xy)
        angle_x = str(round(math.atan(((pixel_x - pixel_center[0]) * pixel_ratio) / z0) * 180 / 3.14 * 10) + x_0)  # Convert the x pixel value into an angle value
        angle_y = str(round(math.atan(((pixel_y - pixel_center[1]) * pixel_ratio) / z0) * 180 / 3.14 * 10) + y_0)  # Convert the y pixel value into an angle value
        posi_z = str(round(z))
        xyz = angle_y.zfill(3) + angle_x.zfill(3) + posi_z.zfill(3)  # Pack xyz as a six-digit 0x0y0z payload
        print('angle: ', int(angle_y) - y_0, "//", int(angle_x) - x_0)
        return xyz

    def send_data(self, xy, z=200):
        # data='SSS'+str(data[0])+','+str(data[0])+','+str(data[0])+'EEE'
        posi = Communication.pixel_to_angle(self, xy, z)
        data = 'SSS' + posi + 'EEE'
        try:
            self.ser.write(data.encode('utf-8'))  # Send one data packet in hex
            # print('send finished:',data)
            return 1

        except Exception as e:
            print("exception, not sent:", e)
            return 0


class find_camera():

    def open_camera(self, cam_n=0, path=None):
        a = False
        if cam_n == 1 or cam_n == 0:
            cap = cv2.VideoCapture(cam_n, cv2.CAP_DSHOW)
            # a=cap.isOpened()
        elif path != None:
            cap = cv2.VideoCapture(path)
        else:
            print("please choose a camera!")

        a = cap.isOpened()
        if a:
            # cv2.namedWindow('Test camera')
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        return cap, a
