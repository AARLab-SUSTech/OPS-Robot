import serial
import time
import numpy as np
from communication import Communication as com
     

class operation:

    def __init__(self, port="COM4",baudrate=9600, timeout=0.03, init_position=[640,360], threshold=30,sampling_time=2,):
        self.init_position = init_position
        self.threshold = threshold
        self.sampling_time = sampling_time
        self.engin1=com(port,baudrate,timeout)
    
    
    def connecting(self):
        ret=self.engin1.connect()
        return ret


    def getfeedback(self):
        data = self.engin1.Recive_data()   
        return data
    
    def send_run(self,position):
        self.engin1.send_data(xy=position,z=200)

    def run_mechine(self,position=[0,0]):
        # operation.run(self,x=900,y=360,z=0)
        times=1
        z_in=130
        dx=250
        dy=100
        x0=position[0]
        y0=position[1]+100
        operation.run(self,x=640,y=200,z=100)
        operation.run(self,x=x0+150,y=y0,z=z_in)

        for i in range(times):
            operation.run(self,x=x0+dx,y=y0+dy,z=z_in)
            operation.run(self,x=x0+dx,y=y0-dy-50,z=z_in)
            operation.run(self,x=x0+dx,y=y0+dy,z=z_in)
            operation.run(self,x=x0+dx,y=y0,z=z_in)

       

        operation.run(self,x=x0+100,y=y0+50,z=z_in)
        operation.run(self,x=x0-100,y=y0,z=z_in)

        for i in range(times):
            operation.run(self,x=x0-dx,y=y0+dy,z=z_in)
            operation.run(self,x=x0-dx,y=y0-dy-50,z=z_in)
            operation.run(self,x=x0-dx,y=y0+dy,z=z_in)
            operation.run(self,x=x0-dx,y=y0,z=z_in)


        operation.run(self,x=x0-150,y=y0,z=100)
        operation.run(self,x=640,y=200,z=100)
        operation.run(self,x=640,y=200,z=1)




    def run(self,x=640,y=360,z=200):
        sig=""
        return_sig=""
        # self.engin1.send("SSS")
        # return_sig = self.engin1.Recive_data()
        # time.sleep(0.01)
        
        while True:
            self.engin1.send("ready")
            return_sig = self.engin1.Recive_data()
            time.sleep(0.01)

            # print("return_sig is",return_sig)
            if return_sig =="4321":
                data=[x,y]
                sig = self.engin1.send_data(xy=data,z=z)
                # print("return_sig is",return_sig)
                break
            else:
                print("waiting")
                time.sleep(0.05)
            return_sig=""    

        return sig
# Engine1 = com("COM5",9600,3)
# op=operation(init_position=[640,360])
# operation().run_mechine()
# com().send_data(xy=[700,400],z=200)



class sendmessage:

    def __init__(self,ser,serialPort="COM5",baudRate=115200):
        self.serialPort = serialPort
        self.baudRate = baudRate
        self.ser = serial.Serial(serialPort,baudRate,timeout = 0.5)
        self.tab=0 #the tab of the former message, 0 means msg from upper computer, 1 means msg from lower computer
        

    def send(self,msg):
        start='SSS'
        end = 'EEE'
        message=str([start,msg,end])
        self.ser.write(message.encode())

    def read(self):
        data = self.ser.readline()  
        data = data.strip()
        data = data.decode('utf-8','ignore')  
        return data

        
    def get_tab(self,data):
        tab=self.ser.readline() 
        data = data.strip()
        data = data.decode('utf-8','ignore')
        if tab==0 or tab==1:
            tab=tab
        else:
            tab=None
        return tab
