from tkinter        import Tk
from check_process  import check_process
from psutil         import net_io_counters
from time           import sleep

class Light(): #灯(色块,纯色悬浮窗口,置顶)
    def __init__(self, color:str, location:str, size:str='4x4'):
        self.root = Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)             # 隐藏标题栏和边框
        self.root.wm_attributes("-toolwindow", True) # 置为工具窗口
        self.root.wm_attributes("-topmost", True)    # 永远处于顶层
        self.root.resizable(False, False)            #横纵均不允许调整
        self.root.configure(bg=color)
        self.root.geometry(size+'+'+location)
        self.root.attributes("-alpha", 1)            # 设置窗口透明度(0为透明,1为不透明)
    def on(self):
        self.root.deiconify()
        self.root.update()
    def off(self):
        self.root.withdraw()
        self.root.update()

def check(name:str, state:list, state_number:int, Light): #检查进程并调整灯的状态
    try:
        process_state = check_process(name)
    except:
        return 0
    if process_state:
        if not state[state_number]:
            Light.on()
            state[state_number] = True
    else:
        if state[state_number]:
            Light.off()
            state[state_number] = False

def low_Ethernet_traffic(): #网速监控(阉割版,只看上传)
    sent_before = net_io_counters().bytes_sent  # 已发送的流量
    #recv_before = net_io_counters().bytes_recv  # 已接收的流量
    sleep(1)
    sent_now = net_io_counters().bytes_sent
    #recv_now = net_io_counters().bytes_recv
    return True if (sent_now - sent_before)<= 102400 else False  # 算出1秒后的差值并判断(单位:Byte) 当前阈值：100KB
    #recv = (recv_now - recv_before)

temp = Tk()
screen_width = temp.winfo_screenwidth()
temp.withdraw()
L1 = Light(color = '#00FF00', location = str(int(screen_width/2-15))+'+0')  # 低网络流量 绿
L2 = Light(color = '#0000FF', location = str(int(screen_width/2-7))+'+0')   #  远程桌面  蓝
L3 = Light(color = '#FF0000', location = str(int(screen_width/2+1))+'+0')   # 摄像头捕获 红
L4 = Light(color = '#FF9300', location = str(int(screen_width/2+9))+'+0')   #  屏幕捕获  橙

state = [False, False, False, False]

while True:
    try:
        check('screenCapture.exe',    state, 3, L4)
        check('media_capture.exe',    state, 2, L3)
        check('rtcRemoteDesktop.exe', state, 1, L2)
    except:
        pass
    if low_Ethernet_traffic(): #低上传流量
        if state[1] or state[2] or state[3]: #任一监控程序运行
            if not state[0]:
                L1.on()
                state[0] = True
        else:
            if state[0]:
                L1.off()
                state[0] = False 
    else:
        if state[0]:
            L1.off()
            state[0] = False
    sleep(1)
