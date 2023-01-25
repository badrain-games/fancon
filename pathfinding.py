import pyxel
import random
import lib
from lib import RectPos
from dataclasses import dataclass

player_speed = 1

@dataclass
class World:
    player_pos = (0,0)
    player_dir = 0
    player_state = "Idle"
    surrounding_grid = [(0,0)] * 8
    angle = 0

world = World()

def is_boundary(x, y):
    _,ty = pyxel.tilemap(0).pget(x // 8, y // 8)
    return ty == 0

def get_block_rect(x, y):
    bx = x // 8 * 8
    by = y // 8 * 8
    return (bx,by,8,8)

def player_rect():
    return (*world.player_pos, 8, 8)

def init():
    pyxel.init(128,128, title="Pathfinding", fps=60, display_scale=4)
    pyxel.load("Assets/pathfinding.pyxres")

    world.player_pos = pyxel.width // 2 - 12, pyxel.height // 2 - 12
    pyxel.run(update, draw)

def update():
    pyxel.cls(0)
    x,y = 0,0
    if pyxel.btn(pyxel.KEY_W):
        y = -1
    if pyxel.btn(pyxel.KEY_S):
        y = 1
    if pyxel.btn(pyxel.KEY_A):
        x = -1
    if pyxel.btn(pyxel.KEY_D):
        x = 1
    dirx,diry = lib.normalize(x,y)
    px,py = world.player_pos

    pyxel.tilemap(0).pget(pyxel.mouse_x // 8, pyxel.mouse_y // 8) 
    px,py = (px + dirx * player_speed, py + diry * player_speed)

    pw,ph = 8,8
    prect = (px,py,pw,ph)
    tl = lib.rect_point(RectPos.TopLeft, prect)
    tr = lib.rect_point(RectPos.TopRight, prect)
    bl = lib.rect_point(RectPos.BottomLeft, prect)
    br = lib.rect_point(RectPos.BottomRight, prect)

    midx,midy,_,_ = get_block_rect(px+4,py+4)
    if is_boundary(*tl):
        brect = get_block_rect(*tl)
        bbrcx,bbrcy = lib.rect_point(RectPos.Center, brect)
        angle = pyxel.atan2(bbrcx-tl[0],bbrcy-tl[1])
        world.angle = f"TL{angle}"
        print(bbrcx, " ", bbrcy, " ", tl[0], " " , tl[1])
        if angle < -123.7:
            px = midx
        else:
            py = midy
    elif is_boundary(*tr):
        brect = get_block_rect(*tr)
        bbrx,bbry = lib.rect_point(RectPos.BottomLeft, brect)
        angle = pyxel.atan2(midx-bbrx,midy-bbry)
        bbrc,bbrc = lib.rect_point(RectPos.Center, brect)
        angle = pyxel.atan2(midx-bbrc,midy-bbrc)
        # world.angle = f"TR{angle}"
        if angle > 75:
            px = midx
        else:
            py = midy
    elif is_boundary(*bl):
        brect = get_block_rect(*bl)
        bbrx,bbry = lib.rect_point(RectPos.TopRight, brect)
        bbrc,bbrc = lib.rect_point(RectPos.Center, brect)
        angle = pyxel.atan2(midx-bbrc,midy-bbrc)
        # world.angle = f"BL{angle}"
        if angle > -135:
            px = midx
        else:
            py = midy
    elif is_boundary(*br):
        brect = get_block_rect(*br)
        bbrx,bbry = lib.rect_point(RectPos.TopLeft, brect)
        bbrc,bbrc = lib.rect_point(RectPos.Center, brect)
        angle = pyxel.atan2(midx-bbrc,midy-bbrc)
        # world.angle = f"BR{angle}"
        if angle > 135:
            px = midx
        else:
            py = midy
     
    world.player_pos = px,py
    if x != 0:
        world.player_dir = 1 if x > 0 else -1
    world.player_state = "Moving" if x != 0 or y != 0 else "Idle"
        

def draw():
    pyxel.bltm(0,0,0,0,0,128,128)

    px, py = world.player_pos
    side = 0 if world.player_dir == -1 else 8
    anim = pyxel.frame_count % 16 // 8 * 8 if world.player_state == "Moving" else 0
    pyxel.blt(px, py, 0, side, anim, 8, 8, 0)

    # for pt in world.surrouding_grid:
    #     x,y,_,_ = get_block_rect(*pt)
    #     pyxel.rect(x+3, y+3, 2, 2, 7)

    tx,ty = pyxel.tilemap(0).pget(pyxel.mouse_x // 8, pyxel.mouse_y // 8)
    pyxel.text(5,3, f"Tile at {pyxel.mouse_x // 8}, {pyxel.mouse_y // 8}: {tx},{ty}", 7)

    pyxel.text(5,10, f"Angle: {world.angle}", 7)


    # dir = pyxel.mouse_x - px, pyxel.mouse_y - py
    # pyxel.text(5,10, f"Angle: {pyxel.atan2(*dir)}", 7)

    color = pyxel.pget(pyxel.mouse_x, pyxel.mouse_y)
    pyxel.blt(pyxel.mouse_x + - 3, pyxel.mouse_y - 3, 0, 0, 16, 8, 8, 0)
    # pyxel.text(5,10, f"Color num: {color}", 7)

init()
