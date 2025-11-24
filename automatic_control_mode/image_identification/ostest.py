


import win32api
import time

app_dir = r'C:\Users\22135\Desktop\相机'
win32api.ShellExecute(0, 'open', app_dir, '','',1)
time.sleep(2)
win32api.ShellExecute(0, 'close', app_dir, '','',1)

  