from pynput.keyboard import Key

isRed    = lambda color: (color[0] > 150) and (color[1] < 80)  and (color[2] < 80)
isGreen  = lambda color: (color[0] < 80)  and (color[1] > 150) and (color[2] < 80)
isBlue   = lambda color: (color[0] < 100) and (color[1] < 150) and (color[2] > 200)
isYellow = lambda color: (color[0] > 150) and (color[1] > 150) and (color[2] < 80)
isPurple = lambda color: (color[0] > 150) and (color[1] < 80)  and (color[2] > 150)
isWhite  = lambda color: (color[0] > 200) and (color[1] > 200) and (color[2] > 200)

ENTER = Key.shift
KEY_COLOR_PAIRS = (
    (isRed,    Key.up),
    (isGreen,  Key.right),
    (isBlue,   Key.down),
    (isYellow, Key.left),
    (isPurple, Key.shift)
)

def getKeyFromColor(color):
    return next((pair[1] for pair in KEY_COLOR_PAIRS if pair[0](color)), None)
