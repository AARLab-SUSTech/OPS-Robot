
import  threading
import time
 
def start_Demo1():
    for i in range(100):
        print("demo1 .....",i)
        time.sleep(1)
 
def start_Demo2():
    for i in range(50):
        print("demo2",i)
        time.sleep(1)
 


a=["a","b","c"]
print(a)
a.pop(0)
print(a)
a.append("d")
print(a)