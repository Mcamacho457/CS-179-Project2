import math

def error(x1, y1, x2, y2):
    e = abs(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    return e