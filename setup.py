import requests
import socket
import openpyxl
import tkinter
import threading
import sys
import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

sys.path.append(os.path.join(sys.path[0],'src'))

executable = Executable(script="client.py", base=base)
options = {
  "build_exe":{
    'include_files':[
         r'C:\Users\Я\AppData\Local\Programs\Python\Python311\Lib\site-packages\idna',
         r'C:\Users\Я\AppData\Local\Programs\Python\Python311\Lib\tkinter',
         r'C:\Users\Я\AppData\Local\Programs\Python\Python311\Lib\threading.py',
         r'C:\Users\Я\AppData\Local\Programs\Python\Python311\Lib\datetime.py',
         r'D:\Python\python_server\functions.py',
         r'C:\Users\Я\AppData\Local\Programs\Python\Python311\Lib\socket.py'
]
  }
}
setup(
  name="Client",
  version="0.1",
  description="Messanger Client",
  requires = ["tkinter", "threading", "datetime", "functions", "socket"],
  options = options,
  executables = [executable]
)