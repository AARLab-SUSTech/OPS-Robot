# import os
# app_dir = r'C:\Users\22135\Desktop\相机'
# os.system(app_dir)


# import os
# import time
# import sys
# def open_app(app_dir):
#   os.startfile(app_dir)
# if __name__ == "__main__":
#   app_dir = r'C:\Users\22135\Desktop\相机'
#   open_app(app_dir)
#   time.sleep(2)
#   os.system("taskkill /F /IM "+app_dir)


import win32api
import time
#日报软件启动
app_dir = r'C:\Users\22135\Desktop\相机'
win32api.ShellExecute(0, 'open', app_dir, '','',1)
time.sleep(2)
win32api.ShellExecute(0, 'close', app_dir, '','',1)

  