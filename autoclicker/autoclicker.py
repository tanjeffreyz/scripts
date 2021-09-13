import mouse
import keyboard
import threading
import win32gui
import winsound
import time


enabled = False
targets = []

delay = 0.1


def mouse_listener():
	global enabled, targets
	while True:
		if keyboard.is_pressed('insert'):
			print('\n\n')
			if not enabled:
				enabled = True
				print('[~] Enabled.')
				winsound.Beep(784, 200)     # G5
			else:
				enabled = False
				print('[~] Disabled.')
				winsound.Beep(523, 200)     # C5
			time.sleep(0.8)
		elif keyboard.is_pressed('end'):
			_, _, target = win32gui.GetCursorInfo()
			targets.append(target)
			print(f'Added a target at {target}.')
			time.sleep(1)
		elif keyboard.is_pressed('del'):
			targets = []
			print('Cleared all targets.')
			time.sleep(1)
		else:
			time.sleep(0.01)


def clicker():
	while True:
		if enabled:
			for pos in targets:
				mouse.move(*pos, absolute=True, duration=0.01)
				mouse.click('left')
				time.sleep(delay)
		else:
			time.sleep(0.01)


if __name__ == '__main__':
	listener_thread = threading.Thread(target=mouse_listener)
	listener_thread.daemon = True
	listener_thread.start()

	main_thread = threading.Thread(target=clicker)
	main_thread.daemon = True
	main_thread.start()

	while True:
		time.sleep(5)