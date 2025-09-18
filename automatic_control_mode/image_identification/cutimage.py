  
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
from cv2 import cv2
import numpy as np

def convertQImageToMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''
    incomingImage = incomingImage.convertToFormat(4)
    width = incomingImage.width()
    height = incomingImage.height()
    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr


def cutpicture(type=None, handle=None):
    hwnd = win32gui.FindWindow( type,handle)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    image = convertQImageToMat(img)
    return image


while 1:
    frame = cutpicture(handle="雷电模拟器")
    
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    cv2.imshow("test", frame)
    cv2.waitKey(1)
    # print(time.time())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 
cv2.destroyAllWindows()