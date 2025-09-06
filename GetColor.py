# SPDX-License-Identifier: MIT
# Copyright (c) 2025 云岭之上

import sys
import tkinter as tk
import win32api
import ctypes

# 设置程序为 DPI 感知
ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1 表示设置为 DPI 感知（System DPI-aware）

# 窗口主程序
win = tk.Tk()  # 建立窗口实例
win.title("GetColor")
win.wm_attributes('-topmost', 1)  # 窗口置顶
win.geometry("340x220+0+0")  # 窗口大小定位
win.wm_attributes('-transparentcolor', '#121212')  # 设置#121212为透明色
win.overrideredirect(True)  # 无标题栏

# 设置画布
cv1 = tk.Canvas(win, width=340, height=220, bg="#121212", highlightthickness=0)  # 画布背景透明色
cv1.place(x=0, y=0)

# 获取光标位置和颜色的函数
def update_info(n):
    try:
        # 清空画布
        cv1.delete(n)

        # 获取光标位置
        x, y = win32api.GetCursorPos()  # 获取当前光标位置
        if x+y == 0:
            sys.exit()
        xy = "XY：" + str(x) + "," + str(y)

        # 获取桌面窗口的 DC
        desktop = ctypes.windll.user32.GetDC(0)
        # 使用 GetPixel 函数获取指定点的颜色
        pixel = ctypes.windll.gdi32.GetPixel(desktop, x, y)
        # 释放桌面窗口的 DC
        ctypes.windll.user32.ReleaseDC(0, desktop)

        # 颜色处理
        r = pixel & 0x0000ff
        g = (pixel & 0x00ff00) >> 8
        b = (pixel & 0xff0000) >> 16

        # RGB 值转换为 HEX 值
        hex_r = format(r, '02x')
        hex_g = format(g, '02x')
        hex_b = format(b, '02x')

        clr = f"RGB：{r},{g},{b}"
        clr2 = f"HEX：#{hex_r}{hex_g}{hex_b}"
        clr3 = f"Pixel：{pixel}"

        # 在画布上显示信息
        cv1.create_text(40, 30, text=xy, fill="#ffffff", font=("Arial", 16), anchor="w")
        cv1.create_text(40, 70, text=clr, fill="#ffffff", font=("Arial", 16), anchor="w")
        cv1.create_text(40, 110, text=clr2, fill="#ffffff", font=("Arial", 16), anchor="w")
        cv1.create_text(40, 150, text=clr3, fill="#ffffff", font=("Arial", 16), anchor="w")
        cv1.create_line(40, 190, 300, 190, fill=f'#{hex_r}{hex_g}{hex_b}', width=30)
        cv1.update()  # 刷新画布

    except Exception as e:
        print(f"Error: {e}")

    win.after(5, update_info,"all")


update_info("all")

win.mainloop()
