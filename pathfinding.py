import pyxel
import random
import lib
from lib import RectPos
from dataclasses import dataclass

@dataclass
class Node:
    index: (int,int)
    edges: list
    visited: bool

@dataclass
class World:
    player_pos = (0,0)
    player_dir = 0
    player_state = "Idle"
    mouse_click = None
    surrounding_grid = [(0,0)] * 8
    path = []
    angle = 0

player_speed = 1.2
world = World()
map_graph = []

def is_boundary(x, y):
    _,ty = pyxel.tilemap(0).pget(x // 8, y // 8)
    return ty == 0

def get_block_rect(x, y):
    bx = x // 8 * 8
    by = y // 8 * 8
    return (bx,by,8,8)

def player_rect():
    return (*world.player_pos, 8, 8)

def generate_graph():
    graph = [None] * (16 * 16)
    for row in range(16):
        for col in range(16):
            if not is_boundary(col * 8, row * 8):
                tiles = lib.get_surrounding_tiles(0, col*8, row*8)
                filtered = filter(lambda xyt: xyt[2] == 1, tiles)
                edges = list(map(lambda xyt: (xyt[1]//8,xyt[0]//8), filtered))
                graph[row * 16 + col] = Node((row,col), edges, False)
    return graph

def debug_print_graph():
    for i,node in enumerate(map_graph):
        if node:
            print(f"Tile {node.index}:")
            for edge in node.edges:
                print("\t", edge)

def get_tile_coord(x,y):
    return y//8,x//8

def get_node_at(row,col):
    idx = int(row * 16 + col)
    return map_graph[idx]

def set_node_at(row,col,val):
    map_graph[int(col // 8 * 16 + col // 8 % 16)]

def dfs(current_node, target_node):
    if current_node == target_node:
        return [target_node]
    elif current_node.visited:
        return []
    else:
        current_node.visited = True
        for n in current_node.edges:
            nn = get_node_at(*n)
            end_node = dfs(nn, target_node)
            if end_node:
                return [current_node] + end_node

def init():
    pyxel.init(128,128, title="Pathfinding", fps=60, display_scale=4)
    pyxel.load("Assets/pathfinding.pyxres")

    global map_graph
    map_graph = generate_graph()
    # debug_print_graph()
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

    def check_boundary(px, py, rect_pos):
        prect = (px,py,pw,ph)
        midx,midy,_,_ = get_block_rect(px+4,py+4)
        point = lib.rect_point(rect_pos, prect)
        pcx,pcy = lib.rect_point(RectPos.Center, prect)
        if is_boundary(*point):
            rx,ry = lib.rect_point(RectPos.Center, get_block_rect(*point))
            distx = round(pcx - rx)             #     -180 _ 180
            disty = round(pcy - ry)             #      /       \
            dir = pyxel.atan2(distx, disty)     # -90 |    x    | 90
            if (dir < -135 or dir > 135         #      \       /
                or (dir >= -45 and dir <= 45)): #          0
                py = midy
            else:
                px = midx
        return (px,py)

    rect_points = ([RectPos.MidTop, RectPos.MidRight, RectPos.MidBottom,
                    RectPos.MidLeft, RectPos.TopLeft, RectPos.TopRight,
                    RectPos.BottomLeft, RectPos.BottomRight])
    for pt in rect_points:
        px,py = check_boundary(px, py, pt)

    global map_graph
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        world.mouse_click = pyxel.mouse_x, pyxel.mouse_y

        player_node = get_node_at(*get_tile_coord(px,py))
        target_node = get_node_at(*get_tile_coord(pyxel.mouse_x,pyxel.mouse_y))
        for node in map_graph:
            if node:
                node.visited = False

        p = dfs(player_node, target_node)
        world.path = p


    world.player_pos = px,py
    if x != 0:
        world.player_dir = 1 if x > 0 else -1
    world.player_state = "Moving" if x != 0 or y != 0 else "Idle"

def mark_tiles(tiles):
    for t in tiles:
        pyxel.rect(t[0]+3, t[1]+3, 2, 2, 7)

def draw():
    pyxel.bltm(0,0,0,0,0,128,128)

    px, py = world.player_pos
    side = 0 if world.player_dir == -1 else 8
    anim = pyxel.frame_count % 16 // 8 * 8 if world.player_state == "Moving" else 0
    pyxel.blt(px, py, 0, side, anim, 8, 8, 0)

    # pcx,pcy = lib.rect_point(RectPos.Center, (px,py,8,8))
    # mark_tiles(lib.get_surrounding_tiles(0,pcx,pcy))

    for n in world.path:
        pyxel.rect(n.index[1]*8+3, n.index[0]*8+3, 2, 2, 7)


    # if world.mouse_click is not None:
    #     mx,my = world.mouse_click
    #     mark_tiles(lib.get_surrounding_tiles(0,mx,my))

    # tx,ty = pyxel.tilemap(0).pget(pyxel.mouse_x // 8, pyxel.mouse_y // 8)
    # pyxel.text(5,3, f"Tile at {pyxel.mouse_y // 8+1}, {pyxel.mouse_x // 8+1}: {tx},{ty}", 7)

    # pyxel.text(5,10, f"Angle: {world.angle}", 7)

    # dir = pyxel.mouse_x - px, pyxel.mouse_y - py
    # pyxel.text(5,10, f"Angle: {pyxel.atan2(*dir)}", 7)

    color = pyxel.pget(pyxel.mouse_x, pyxel.mouse_y)
    pyxel.blt(pyxel.mouse_x + - 3, pyxel.mouse_y - 3, 0, 0, 16, 8, 8, 0)
    # pyxel.text(5,10, f"Color num: {color}", 7)

init()
