import pyxel
import random
import lib
from lib import RectPos
from dataclasses import dataclass

player_speed = 0.9

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

    def check_boundary(px, py, corner):
        prect = (px,py,pw,ph)
        midx,midy,_,_ = get_block_rect(px+4,py+4)
        point = lib.rect_point(corner, prect)
        pcx,pcy = lib.rect_point(RectPos.Center, prect)
        if is_boundary(*point):
            rx,ry = lib.rect_point(RectPos.Center, get_block_rect(*point))
            distx = round(pcx - rx)
            disty = round(pcy - ry)
            dir = pyxel.atan2(distx, disty)
            if dir < -135 or dir > 135 or (dir >= -45 and dir <= 45):
                py = midy
            else:
                px = midx
        return (px,py)

    px,py = check_boundary(px, py, RectPos.MidTop)
    px,py = check_boundary(px, py, RectPos.MidRight)
    px,py = check_boundary(px, py, RectPos.MidBottom)
    px,py = check_boundary(px, py, RectPos.MidLeft)
    px,py = check_boundary(px, py, RectPos.TopLeft)
    px,py = check_boundary(px, py, RectPos.TopRight)
    px,py = check_boundary(px, py, RectPos.BottomLeft)
    px,py = check_boundary(px, py, RectPos.BottomRight)

    #     -180 - 180
    #      /       \
    # -90 |         | 90
    #      \       /
    #          -
    #          0


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

    # pyxel.text(5,10, f"Angle: {world.angle}", 7)

    # dir = pyxel.mouse_x - px, pyxel.mouse_y - py
    # pyxel.text(5,10, f"Angle: {pyxel.atan2(*dir)}", 7)

    color = pyxel.pget(pyxel.mouse_x, pyxel.mouse_y)
    pyxel.blt(pyxel.mouse_x + - 3, pyxel.mouse_y - 3, 0, 0, 16, 8, 8, 0)
    # pyxel.text(5,10, f"Color num: {color}", 7)

init()
