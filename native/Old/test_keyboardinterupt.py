from time import time
from tkinter import messagebox, Tk

root = Tk()
root.attributes("-topmost", True)
root.withdraw()  # 隱藏主視窗

start_time = time()
try:
    while True:
        if time() - start_time > 2:
            print("2 秒")
            start_time = time()
        pass
except KeyboardInterrupt:
    messagebox.showinfo("Info", "Test keyboard interrupt")
finally:
    messagebox.showinfo("Info", "end")
