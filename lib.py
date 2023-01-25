import pyxel
import enum

def normalize(x, y):
    if x == 0 and y == 0:
        return (x,y)
    magnitude = pyxel.sqrt(x**2 + y**2)
    return (x / magnitude, y / magnitude)

class RectPos(enum.Enum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3
    Center = 4

def rect_contains(rect, point):
    rx,ry,w,h = rect
    x,y = point
    return x > rx and x < rx + w and y > ry and y < ry + h

def rect_point(point, rect):
    x,y,w,h = rect
    match point:
        case RectPos.TopLeft:
            return (x,y)
        case RectPos.TopRight:
            return (x+w,y)
        case RectPos.BottomLeft:
            return (x,y+h)
        case RectPos.BottomRight:
            return (x+w,y+h)
        case RectPos.Center:
            return (x+w/2,y+h/2)

