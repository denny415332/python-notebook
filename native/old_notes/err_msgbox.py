import tkinter as tk
from tkinter import messagebox


def show_error():
    try:
        # 模擬引發錯誤
        result = 1 / 0
    except Exception as e:
        # 彈出錯誤視窗
        messagebox.showerror("錯誤", f"發生錯誤：{e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    show_error()
