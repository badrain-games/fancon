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

def draw9s(x, y, u, v, w, h, cx, cy, tc):
    w2 = 16-cx
    h2 = 16-cy
    # TL Corner
    pyxel.blt(x, y, 0, u, v, cx, cy, tc)
    # TR Corner
    pyxel.blt(x + w - w2, y, 0, u + cx, v, w2, cy, tc)
    # BL Corner
    pyxel.blt(x, y + h - h2, 0, u, v + cy, cx, h2, tc)
    # BR Corner
    pyxel.blt(x + w - w2, y + h - h2, 0, u + cx, v + cy, w2, h2, tc)

    # Left Line
    for p in range(cx):
        color = pyxel.image(0).pget(u + p, v + cy-1)
        if color != tc:
            pyxel.line(x+p, y+cy, x+p, y+h-h2-1, color)
    # Top Line
    for p in range(cy):
        color = pyxel.image(0).pget(u+cx-1, v+p)
        if color != tc:
            pyxel.line(x+cx, y+p, x+w-w2-1, y+p, color)
    # Bottom Line
    for p in range(h2):
        color = pyxel.image(0).pget(u+cx-1, v+cy+p)
        if color != tc:
            pyxel.line(x+cx, y+h-h2+p, x+w-cx, y+h-h2+p, color)
    # Right Line
    for p in range(cx):
        color = pyxel.image(0).pget(u+cx+p, v+cy-1)
        if color != tc:
            pyxel.line(x+w+p-cx, y+cy, x+w+p-cx, y+h-h2-1, color)

    # Subtract cx and cy by 1 because the pixels are 0 indexed
    center_color = pyxel.image(0).pget(u + cx-1, v + cy-1)
    pyxel.rect(x+cx, y+cy, w-16, h-16, center_color)

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
