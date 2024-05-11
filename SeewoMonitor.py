#程序作用:监控进程
#当指定的程序运行时弹出红点提示
import tkinter as tk
from threading import Thread, Event
import psutil, time

#要监控的进程名, 忽略大小写 #测试用         媒体捕获
process_name = ['Print_arguments.exe','media_capture.exe']
for i in range(len(process_name)):
    process_name[i] = process_name[i].lower()
frequency = 1   #检测间隔时间

def show(stop_event):
    class FloatingWindow(tk.Toplevel):
        def __init__(self, master=None, **kwargs):
            super().__init__(master, **kwargs)
            self.overrideredirect(True)  # 隐藏标题栏和边框
            self.attributes("-alpha", 1)  # 设置窗口透明度(0为透明,1为不透明)
            self.wm_attributes("-toolwindow", True)  # 置为工具窗口(没有最大最小按钮)
            self.wm_attributes("-topmost", True)     # 永远处于顶层
            self.configure(bg='red')
            self.resizable(False, False) #横纵均不允许调整       
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    floating_window = FloatingWindow(root)
    screen_width = root.winfo_screenwidth()
    floating_window.geometry("4x4+"+str(int(screen_width/2))+"+0")

    def check_stop():
        if not stop_event.is_set():
            floating_window.after(frequency * 1000, check_stop)
        else:
            floating_window.destroy()
            root.destroy()
    check_stop()
    root.mainloop()

def check_process():
    processes = psutil.process_iter()
    for process in processes:
    	if process.name().lower() in process_name :
    	    return True
    return False

stop_event = Event()
flag = False    #False表示没运行,Tuee表示运行

while True:
    if flag != check_process():
        flag = not flag     #布尔值翻转
        if flag:
            t1 = Thread(target=show,args=(stop_event,))
            try:
                t1.start()
            except:
                flag == False
        else:
            stop_event.set()
            t1.join()
            stop_event.clear()
    time.sleep(frequency)

