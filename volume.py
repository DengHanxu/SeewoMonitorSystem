from ctypes		 import cast, POINTER
from comtypes	 import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class volume():
	
	def __init__(self):
		self.devices = AudioUtilities.GetSpeakers()
		self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
		self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
	
	def is_mute(self):
		return self.volume.GetMute()

	def set_mute(self, state):
                self.volume.SetMute(state, None)
	
	def get_range(self):
		return self.volume.GetVolumeRange()
	
	def get_level(self):
		return self.volume.GetMasterVolumeLevel()
	
	def set_level(self, level):
		self.volume.SetMasterVolumeLevel(level, None)

if __name__ == '__main__':
    vol = volume()
    print('静音',vol.is_mute())
    print('范围',vol.get_range())
    print('音量值',vol.get_level())
    vol.set_level(float(input('设置音量值> ')))
    input('按[Enter]退出')
