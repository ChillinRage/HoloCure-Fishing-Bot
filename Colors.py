def isRed(color):
    return (color[0] > 150) and (color[1] < 80)  and (color[2] < 80)

def isGreen(color):
    return (color[0] < 80)  and (color[1] > 150) and (color[2] < 80)

def isBlue(color):
    return (color[0] < 100) and (color[1] < 150) and (color[2] > 200)

def isYellow(color):
    return (color[0] > 150) and (color[1] > 150) and (color[2] < 80)

def isPurple(color):
    return (color[0] > 150) and (color[1] < 80)  and (color[2] > 150)

def isWhite(color):
    return (color[0] > 200) and (color[1] > 200) and (color[2] > 200)
