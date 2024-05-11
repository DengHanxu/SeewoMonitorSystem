from check_process  import check_process
from playsound      import playsound
from time           import sleep
from volume         import volume

state = False
vol=volume()

def ring(sound):
    try:
        vol.set_mute(0)
        current_vol = vol.get_level()
        if current_vol < -10.5:
            vol.set_level(-10.5)
        playsound(sound)
        if current_vol < -10.5:
            vol.set_level(current_vol)
    except:
        pass

while True:
    try:
        process_state = check_process('media_capture.exe')
    except:
        sleep(0.5)
        continue
    if process_state:
        if not state:
            ring("C:\\Windows\\Media\\Windows Hardware Insert.wav")
            state = True
    else:
        if state:
            ring("C:\\Windows\\Media\\Windows Hardware Remove.wav")
            state = False
    sleep(2)
