import time, threading, pyautogui
import KeyColors
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
        key = KeyColors.getKeyFromColor(pixel)
        if key: return key
    return None

def isWhiteFrame():
    '''checks if a frame contains only white pixels'''
    frame = ImageGrab.grab(bbox = WHITE_FRAME_BOX).getdata()
    for pixel in frame:
        if not KeyColors.isWhite(pixel):
            return False
    return True

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

    def checkFrame(self):
        key = getImageKey()
        if key:
            self.press(key)
        elif isWhiteFrame(): # check if result screen is showing
            self.press(KeyColors.ENTER)
            time.sleep(0.7)
            self.press(KeyColors.ENTER)

    def run(self):
        while self.programRunning:
            while self.running:
                threading.Thread(target=self.checkFrame, args=()).start()
                time.sleep(0.02)
            time.sleep(0.1)

def on_press(key):
    if key == TRIGGER_KEY:
        if main_thread.running:
            main_thread.pause()
        else:
            main_thread.resume()

    elif key == EXIT_KEY:
        main_thread.exit()
        listener.stop()

if __name__ == "__main__":
    print("Press 'z' to start and stop the program")
    print("Press 'x' to close the program and window")

    keyboard = Controller()
    main_thread = KeyPresser(keyboard)
    main_thread.start()

    with Listener(on_press = on_press) as listener:
        listener.join()

    print("Closing program...")
