import time, threading, pyautogui
import Colors, Keys
from PIL import ImageGrab
from pynput.keyboard import KeyCode, Controller, Listener

TRIGGER_KEY = KeyCode(char="z") # start/pause program
EXIT_KEY    = KeyCode(char="x") # close program

WIDTH = pyautogui.size().width
HEIGHT = pyautogui.size().height

KEY_FRAME_BOX = (
    int(WIDTH * 0.61),
    int(HEIGHT * 0.69),
    int(WIDTH * 0.61) + 25,
    int(HEIGHT * 0.69) + 10
)

WHITE_FRAME_BOX = (
    int(WIDTH * 0.53),
    int(HEIGHT * 0.72),
    int(WIDTH * 0.53) + 4,
    int(HEIGHT * 0.72) + 4
)

def getImageKey():
    '''returns the keyboard key for the current frame'''
    frame = ImageGrab.grab(bbox = KEY_FRAME_BOX).getdata()
    for pixel in frame:
        if Colors.isRed(pixel):      return Keys.red
        elif Colors.isGreen(pixel):  return Keys.green
        elif Colors.isBlue(pixel):   return Keys.blue
        elif Colors.isYellow(pixel): return Keys.yellow
        elif Colors.isPurple(pixel): return Keys.purple
    return None

def isWhiteFrame():
    '''checks if a frame contains only white pixels'''
    frame = ImageGrab.grab(bbox = WHITE_FRAME_BOX).getdata()
    for pixel in frame:
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
        time.sleep(0.03)
        self.keyboard.release(key)

    def run(self):
        while self.programRunning:
            while self.running:
                key = getImageKey()
                if key:
                    self.press(key)
                elif isWhiteFrame(): # check if result screen is showing
                    self.press(Keys.enter)
                    time.sleep(0.7)
                    self.press(Keys.enter)
            time.sleep(0.05)


if __name__ == "__main__":
    print("Press 'z' to start and stop the program")
    print("Press 'x' to close the program and window")

    keyboard = Controller()
    main_thread = KeyPresser(keyboard)
    main_thread.start()

    with Listener(on_press = on_press) as listener:
        listener.join()


    
    



