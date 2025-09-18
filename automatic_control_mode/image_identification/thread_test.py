
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
 
# if __name__ == "__main__":
#         t1 = threading.Thread(target=start_Demo1)
#         t2 = threading.Thread(target=start_Demo2)
#         print("第1次循环开始："  + time.ctime())
#         t1.start()  # 当调用start()时，才会真正的创建线程，并且开始执行
#         t2.start()  # 启动线程，即让线程开始执行
#         print("第1次循环结束："  + time.ctime())

a=["a","b","c"]
print(a)
a.pop(0)
print(a)
a.append("d")
print(a)