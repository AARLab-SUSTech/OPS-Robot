
import cv2
import time


def open_camera(cam_n=1):
    a=False
    # while i<20:
    cap = cv2.VideoCapture(cam_n)#, cv2.CAP_DSHOW)
    a=cap.isOpened()
    if a:
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 748)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 486)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    return cap,a

cap,retu=open_camera(cam_n=1)
print(retu)
while retu:
    ret, frame = cap.read()
 
    cv2.imshow("test", frame)
 
    # print(time.time())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
 