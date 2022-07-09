import mouse
import keyboard
import threading
import win32gui
import winsound
import time


enabled = False
targets = []

# Settings
delay = 5
start = '['
add = ']'
clear = '\\'
increment = 'up'
decrement = 'down'


def listener():
	global enabled, targets, delay
	while True:
		if keyboard.is_pressed(start):
			print('\n\n')
			if not enabled:
				enabled = True
				print('[~] Enabled.')
				print(f'Targets: {targets}')
				winsound.Beep(784, 200)     # G5
			else:
				enabled = False
				print('[~] Disabled.')
				winsound.Beep(523, 200)     # C5
			time.sleep(0.8)
		elif keyboard.is_pressed(add):
			_, _, target = win32gui.GetCursorInfo()
			targets.append(target)
			print(f'Added a target at {target}.')
			time.sleep(1)
		elif keyboard.is_pressed(clear):
			targets = []
			print('Cleared all targets.')
			time.sleep(1)
		# elif keyboard.is_pressed(increment):
		# 	delay += 1
		# 	print(f'Increased delay to {delay} seconds.')
		# 	time.sleep(0.667)
		# elif keyboard.is_pressed(decrement):
		# 	delay -= 1
		# 	print(f'Decreased delay to {delay} seconds.')
		# 	time.sleep(0.667)
		else:
			time.sleep(0.01)


def clicker():
	while True:
		if enabled:
			for pos in targets:
				if enabled:
					mouse.move(*pos, absolute=True, duration=0.01)
					mouse.click('left')
					time.sleep(delay)
		else:
			time.sleep(0.01)


if __name__ == '__main__':
	listener_thread = threading.Thread(target=listener)
	listener_thread.daemon = True
	listener_thread.start()

	main_thread = threading.Thread(target=clicker)
	main_thread.daemon = True
	main_thread.start()

	print('AutoClicker controls:')
	print(f"    Start/stop          |   {start}")
	print(f"    Add target          |   {add}")
	print(f"    Clear all targets   |   {clear}")
	# print(f"    Increase delay      |   {increment}")
	# print(f"    Decrease delay      |   {decrement}")
	while True:
		time.sleep(5)
