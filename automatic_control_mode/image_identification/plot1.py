import numpy as np
import time
import matplotlib.pyplot as plt
import cv2


def one2matrix(data):
    N=len(data) 
    num_matrix=np.ones((N,40))
    for i in range(N):
        if i<40:
            num_matrix[i,0:i]=data[0:i]
        if i>=40:
            num_matrix[i,:]=data[(i-40):i]
    return num_matrix

def draw_figure(y,i):
    z=np.ones((40,1))
    z1=np.ones((40,1))*40
    x = np.linspace(0, len(y), len(y))
    plt.figure()    # 定义一个图像窗口
    plt.plot(x, y,linewidth=4,color='r') # 绘制曲线 y1
    # plt.plot(x,z, linestyle="-",linewidth=4,color='k')
    plt.plot(x,z1, linestyle="-",linewidth=2,color='b')
    # plt.plot(0,50, linestyle="-",linewidth=4,color='b')
    plt.xlim(0,40)
    plt.ylim(0,100)
    # plt.xlabel("Samples",fontsize=12,   )
    # plt.ylabel("Motor current (mA)",fontsize=24   )
    plt.xticks([])
    plt.yticks([])
    # plt.show()
    # 设置横轴精准刻度
    # plt.xticks([0,5,10,15,20],fontsize=12,)
    # # 设置纵轴精准刻度
    # plt.yticks(np.linspace(0,120,2),fontsize=12,)
    # plt.axis('off')
    plt.savefig("D:/throat swab/video/code/fig19/fig"+str(i)+".png")
    plt.close()

    cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
    img = cv2.imread("D:/throat swab/video/code/fig19/fig"+str(i)+".png")
    # cv2.imshow('image',img) 
    # cv2.waitKey(0)
    return img



videoname="4_19_human_demo"
file_path="D:/throat swab/video/test_video/"
file1='dataset_'+videoname+'.mp4' 
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # mp4
# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
size=(640,480)
out = cv2.VideoWriter(file_path+file1,fourcc,25,size)

# data=np.random.random(500)*100    # 随机数组/矩阵(float型)，（3行，5列）
# print(np.shape(data))
# print(data[0:2])
# # data=[225,211.1,210.43,204.14,186.81,206.78,211.69,192.88,217.45,205.25,239.77,226.02,216.67,205.74,219.15,223.62,208.81,205.83,224.89,217.5]
# np.savetxt("force_list.txt",data)


data=np.loadtxt("D:/throat swab/video/code/list/force_list_"+videoname+".txt")
print(len(data))
# data=data[40:300]
# for i in range(1,len(data)-1):
#     if data[i]<60:
#         data[i]=0.5*(data[i-1]+data[i+1])
    # data[i]=(data[i]+data[i+1]+data[i+2]+data[i+3])/4

# print(np.shape(data))
# print(data[0,:])


i=0
data_mat=one2matrix(data)
print(data_mat)
for num in data_mat:
    s=time.time()
    i=i+1
    print(num[19])
    image=draw_figure(num,i)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
    cv2.imshow('image',image) 
    cv2.waitKey(1)
    out.write(image)
    e=time.time()
    # break
    # print(e-s)
    # out.imwrite(file_path+'picture/'+str(i)+'.jpg',image)
out.release()



