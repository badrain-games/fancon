import pyxel
import enum

def mag(x,y):
    return pyxel.sqrt(x**2 + y**2)

def distance(p1, p2):
    x = (p2[0] * 8 + 3) - (p1[0] * 8 + 3)
    y = (p2[1] * 8 + 3) - (p1[1] * 8 + 3)
    return mag(x, y)

def normalize(x, y):
    if x == 0 and y == 0:
        return (x,y)
    m = mag(x, y)
    return (x/m, y/m)

class RectPos(enum.Enum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3
    Center = 4
    MidTop = 5
    MidBottom = 6
    MidLeft = 7
    MidRight = 8

tiles = ([(0,-8), (-8,0),(8,0), (0,8)])

def get_surrounding_tiles(tile_map, tx,ty):
    def get_tile_info(xy):
        x = tx + xy[0]
        y = ty + xy[1]
        t = pyxel.tilemap(tile_map).pget(x // 8, y // 8)[1]
        return (x // 8 * 8,y // 8 * 8,t)
    return list(map(get_tile_info, tiles))

def rect_has_point(rect, point):
    rx,ry,w,h = rect
    x,y = point
    return x >= rx and x <= rx + w and y >= ry and y <= ry + h

def rect_overlaps(r1, r2):
    r1x,r1y,r1w,r1h = r1
    r2x,r2y,r2w,r2h = r2
    if ((r1x > r2x and r1x < r2x + r2w and r1y > r2y and r1y < r2y + r2h)
        or
        (r2x > r2x and r1x < r2x + r2w and r1y > r2y and r1y < r2y + r2h)):
        return True

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
        case RectPos.MidTop:
            return (x+w/2,y)
        case RectPos.MidBottom:
            return (x+w/2,y+h)
        case RectPos.MidLeft:
            return (x,y+h/2)
        case RectPos.MidRight:
            return (x+w,y+h/2)
