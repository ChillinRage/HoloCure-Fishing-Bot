import Colors
import Keys
import time
import threading
from PIL import ImageGrab
from pynput.keyboard import KeyCode, Controller, Listener

TRIGGER_KEY = KeyCode(char="z") # start/pause program
EXIT_KEY    = KeyCode(char="x") # close program

def getImageKey():
    image = ImageGrab.grab(bbox = (1175, 750, 1200, 760))
    for x in range(25):
        for y in range(10):
            pixel = image.getpixel((x,y))
            if Colors.isRed(pixel):      return Keys.red
            elif Colors.isGreen(pixel):  return Keys.green
            elif Colors.isBlue(pixel):   return Keys.blue
            elif Colors.isYellow(pixel): return Keys.yellow
            elif Colors.isPurple(pixel): return Keys.purple
    return None

def checkOK():
    image = ImageGrab.grab(bbox = (870, 810, 874, 814))
    for x in range(4):
        for y in range(4):
            pixel = image.getpixel((x,y))
            if not Colors.isWhite(pixel):
                return False
    return True

def on_press(key):
    if key == TRIGGER_KEY:
        if main_thread.running:
            main_thread.pause()
        else:
            main_thread.resume()
    elif key == EXIT_KEY:
        main_thread.exit()
        listener.stop()

class KeyPresser(threading.Thread):
    def __init__(self, keyboard):
        super(KeyPresser, self).__init__()
        self.keyboard = keyboard
        self.running = False  # changed by trigger key
        self.programRunning = True  # changed by exit key

    def resume(self):
        print('Resuming')
        self.running = True
    def pause(self):
        print('Pausing')
        self.running = False
    def exit(self):
        self.pause()
        self.programRunning = False

    def press(self, key):
        self.keyboard.press(key)
        time.sleep(0.04)
        self.keyboard.release(key)

    def run(self):
        while self.programRunning:
            while self.running:
                key = getImageKey()
                if key:
                    self.press(key)
                elif checkOK(): # check if result screen showing
                    self.press(Keys.enter)
                    time.sleep(0.8)
                    self.press(Keys.enter)
            time.sleep(0.1)

if __name__ == "__main__":
    print("Starting...")
    print("Press 'z' to start and stop the program.\n"
          "Press 'x' to close the program."
          )

    keyboard = Controller()
    main_thread = KeyPresser(keyboard)
    main_thread.start()

    with Listener(on_press = on_press) as listener:
        listener.join()
