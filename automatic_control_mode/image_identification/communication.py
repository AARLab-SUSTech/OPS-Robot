import serial
import serial.tools.list_ports
import time
import cv2
import math

class Communication():

    #初始化
    def __init__(self,com='COM4',bps=9600,timeout=0.05):
        self.port = com
        self.bps = bps
        self.timeout =timeout
        global Ret
        Ret=False
        try:
            # 打开串口，并得到串口对象
             self.ser= serial.Serial(self.port,self.bps,timeout=self.timeout)
            # 判断是否打开成功
             if (self.ser.is_open):
               Ret = True
        except Exception as e:
            print("---异常---serial not oppen：", e)

    

    def if_Open_Ser(self):
        return_sig="",
        Ret=self.engin1.Open_Engine()
        if Ret==True:
            self.engin1.send("SSS")
            return_sig = self.engin1.Recive_data()
            time.sleep(0.01)

        return return_sig

    def connect(self):
        Ret_sig=""
        ret=0
        while(1):
            if Ret==True:
                self.send("ready")
                print("sended ready")
                Ret_sig = self.Recive_data()
                time.sleep(0.01)
            else:
                print("Please connect the Bluetooth...")

            if Ret_sig=="4":
                ret=1
                print("received:",Ret_sig)
                print("connected...")
                break
            else:
                print("Waiting connection feedback......")
                print(Ret_sig)
            time.sleep(1)
        return ret

    def Open_Engine(self):
        return Ret

    #关闭串口
    def Close_Engine(self):
        self.ser.close()
        print(self.ser.is_open)  # 检验串口是否打开
    
    def send(self,data):
        try:
            self.ser.write(data.encode('utf-8'))
        except Exception as e:
            print("异常报错 no send：",e)



    def Recive_data(self,):
        # 循环接收数据，此为死循环，可用线程实现
        data='no data'
        data = self.ser.readline()#方式二print("接收ascii数据：", data)
        data = data.strip()
        data = data.decode('utf-8','ignore')   
        time.sleep(0.001)
        return data

    # def Recive_data(self,):
    #     # 循环接收数据，此为死循环，可用线程实现
    #     data='no data'
    #     try:
    #         data = self.ser.readline()#方式二print("接收ascii数据：", data)
    #         data = data.strip()
    #         data = data.decode('utf-8','ignore')   
    #         time.sleep(0.002)

    #     except Exception as e:
    #         print("异常报错 no received data!：",e)
    #         data=None
    #     return data

    def pixel_to_angle(self,xy,z):
        pixel_x=xy[0]
        pixel_y=xy[1]
        pixel_center = [640,150]  
        pixel_ratio = 0.05
        z0 =175
        x_0=510
        y_0=665
        print("xy",xy)
        angle_x = str(round(math.atan( ( (pixel_x - pixel_center[0]) *pixel_ratio) / z0) *360/3.14*10)+x_0) #将x的像素值转换为角度值
        angle_y = str(round(math.atan( ( (pixel_y - pixel_center[1] ) *pixel_ratio) / z0) *360/3.14*10)+y_0) #将y的像素值转换为角度值
        posi_z=str(round(z))
        xyz = angle_y.zfill(3) + angle_x.zfill(3) + posi_z.zfill(3) #将xyz表示为0x0y0zd的六位数据
        print('angle: ',int(angle_y)-y_0,"//",int(angle_x)-x_0)
        return xyz

    def send_data(self,xy,z=200):
        # data='SSS'+str(data[0])+','+str(data[0])+','+str(data[0])+'EEE'
        posi = Communication.pixel_to_angle(self,xy,z)
        data='SSS'+posi+'EEE'
        try:
            self.ser.write(data.encode('utf-8'))  # 十六制发送一个数据
            # print('send finished:',data)
            return 1

        except Exception as e:
            print("异常报错 not sended：",e)
            return 0
        


class find_camera():

    def open_camera(self,cam_n=0, path=None):
        a=False
        if cam_n==1 or cam_n==0:
            cap = cv2.VideoCapture( cam_n , cv2.CAP_DSHOW)
            # a=cap.isOpened()
        elif path != None :
            cap = cv2.VideoCapture( path )
        else:
            print("please choose a camera!")

        a=cap.isOpened()
        if a:
            # cv2.namedWindow('Test camera')
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        return cap,a

