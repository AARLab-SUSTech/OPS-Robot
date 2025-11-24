import numpy as np
n=0
# L=np.zeros(3,5001)
# M=np.zeros(3,5001)
# H=np.zeros(3,5001)
with open("D:/throat swab/video/arduino code/HEX.txt","w+") as f:
    f.write("\nlow position:\n")
    for i in range(0,10000):
        # print(i)
        # b ='0x%02X'%(i//256)
        L ='0x%02X'%(i%256)
        if i%10==0:
            n+=1
            f.write(L+",")
        if i%300==0:
            f.write('\\\n')
    f.write("\nmedia position:\n")        
    for i in range(0,10000):
        # print(i)
        # b ='0x%02X'%(i//256)
        M ='0x%02X'%(i//256)
        if i%10==0:
            f.write(M+",")
        if i%300==0:
            f.write('\\\n')
    f.write("\nhigh position:\n")
    # for i in range(0,5001):
    #     # print(i)
    #     # b ='0x%02X'%(i//256)
    #     H ='0x%02X'%(i%256)

    #     f.write(H+",")
    #     if i%10==0:
    #         f.write('\n')
    print(hex(9000))
    print(n)