from psutil         import net_io_counters
from time           import sleep
from check_process  import check_process
from subprocess     import run, check_output
from os             import system

count = 0
while True:
    try:
        process_state = check_process(['media_capture.exe','screenCapture.exe','rtcRemoteDesktop.exe'])
    except:
        sleep(0.5)
        continue
    if process_state:
        sent_before = net_io_counters().bytes_sent
        sleep(1)
        sent_now = net_io_counters().bytes_sent
        if sent_now - sent_before < 102400: #上传网速小于100KB/S
            count += 1
        if count >= 60:
            try:
                check_output('Nsudo -U:S -ShowWindowMode:Hide taskkill /f /im media_capture.exe', shell=True)
                check_output('Nsudo -U:S -ShowWindowMode:Hide taskkill /f /im screenCapture.exe', shell=True)
                check_output('Nsudo -U:S -ShowWindowMode:Hide taskkill /f /im rtcRemoteDesktop.exe', shell=True)
            except:
                pass
    else:
        count = 0
        sleep(1)
