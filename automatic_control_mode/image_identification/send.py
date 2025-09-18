import serial
import time
from communication import Communication 



Ret =False #是否创建成功标志

Engine1 = Communication("COM4",9600,3)
Ret=Engine1.Open_Engine()
print(Ret)
if (Ret):
    i=1
    while 1:
        i+=1
        # data_input = input("Enter your input: ")
        # print('your input is: ',data_input)
        # # data_input=20
        # Engine1.send_data(xy=data_input)
        data = Engine1.Recive_data()

           
        # data1 = Engine1.Read_Line()
        print('receive data:',data)
        # print(data1)
        time.sleep(0.01)

