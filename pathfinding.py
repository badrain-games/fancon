import pyxel
import random
import lib
import math
from collections import deque
from lib import RectPos
from dataclasses import dataclass
from lib import draw9s

@dataclass
class Node:
    index: (int,int)
    edges: list
    visited: bool
    processed: bool
    parent: None
    g = 99999
    h = 99999

@dataclass
class World:
    player_pos = (0,0)
    player_dir = 0
    player_state = "Idle"
    heap = []
    start_node = None
    target_node = None
    path = []
    current_alg = "A_Star"
    help_ui_active = False

def is_boundary(x, y):
    _,ty = pyxel.tilemap(0).pget(x // 8, y // 8)
    return ty == 0

def get_block_rect(x, y):
    bx = x // 8 * 8
    by = y // 8 * 8
    return (bx,by,8,8)

def get_node_pos(node):
    return node.index[1] * 8 + 4, node.index[0] * 8 + 4

def generate_graph():
    graph = [None] * (16 * 16)
    for row in range(16):
        for col in range(16):
            if not is_boundary(col * 8, row * 8):
                tiles = lib.get_surrounding_tiles(0, col*8, row*8)
                filtered = filter(lambda xyt: xyt[2] == 1, tiles)
                edges = list(map(lambda xyt: (xyt[1]//8,xyt[0]//8), filtered))
                graph[row * 16 + col] = Node((row,col), edges, False, False, None)
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
    if row >= 0 and row < 16 and col >= 0 and col < 16:
        idx = int(row * 16 + col)
        return map_graph[idx]

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

def bfs(start_node, target_node):
    if start_node == target_node:
        return [target_node]

    q = deque()
    q.append(start_node)
    path = []
    found = False
    while q and not found:
        n = q.popleft()
        if n == target_node:
            current = n
            path.append(n)
            while True:
                if current.parent:
                    path.append(current.parent)
                    current = current.parent
                else:
                    found = True
                    break
        else:
            n.visited = True
            for erow,ecol in n.edges:
                edge_node = get_node_at(erow,ecol)
                if not edge_node.visited:
                    edge_node.parent = n
                    q.append(edge_node)
    path.reverse()
    return path

def astar_init(start_node, target_node):
    if target_node is None:
        return []
    world.path = []
    world.heap = [start_node]
    world.start_node = start_node
    world.target_node = target_node
    start_node.processed = True


def astar_update(start_node, target_node):
    heap = world.heap
    if heap:
        node = heap[0]
        if node == target_node:
            while node.parent is not None:
                world.path.append(node)
                node = node.parent
            world.path.reverse()
            world.heap = []
            return

        node.processed = True
        for edge in node.edges:
            nn = get_node_at(*edge)
            if not nn.processed:
                nn.h = lib.distance(get_node_pos(nn), get_node_pos(world.target_node)) * 1.2
                nn.g = g_cost + node.g if node.parent else g_cost
                nn.parent = node
                if nn not in heap:
                    nn.visited = True
                    heap.append(nn)
        heap.pop(0)
        heap.sort(key=lambda n: n.g + n.h)

def update():
    pyxel.cls(0)

    if pyxel.btnp(pyxel.KEY_SLASH) and pyxel.btn(pyxel.KEY_SHIFT):
        world.help_ui_active = not world.help_ui_active
    if pyxel.btnp(pyxel.KEY_Q):
        world.help_ui_active = False

    if pyxel.btn(pyxel.KEY_1):
        world.current_alg = "A_Star"
    if pyxel.btn(pyxel.KEY_2):
        world.current_alg = "DFS"
    if pyxel.btn(pyxel.KEY_3):
        world.current_alg = "BFS"

    if world.help_ui_active:
        return

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

    if world.path:
        n = world.path[0]
        nx,ny = get_node_pos(n)
        pcx,pcy = px+4,py+4
        dir = lib.normalize(nx - pcx, ny - pcy)
        pcx,pcy = (pcx + dir[0] * player_speed * 0.5, pcy + dir[1] * player_speed * 0.5)
        dist = lib.distance((nx,ny), (pcx,pcy))
        if dist < 0.8:
            pcx,pcy = nx,ny
            del world.path[0]
        x = dir[0]
        px,py = pcx-4,pcy-4

    global map_graph
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        player_node = get_node_at(*get_tile_coord(px,py))
        target_node = get_node_at(*get_tile_coord(pyxel.mouse_x,pyxel.mouse_y))
        for node in map_graph:
            if node:
                node.visited = False
                node.processed = False
                node.parent = None
                node.g = 9999999
                node.h = 9999999

        if world.current_alg == "DFS":
            p = dfs(player_node, target_node)
            world.path = p

        if world.current_alg == "BFS":
            p = bfs(player_node, target_node)
            world.path = p

        if world.current_alg == "A_Star":
            astar_init(player_node, target_node)
            astar_update(player_node, target_node)


    if pyxel.btnp(pyxel.KEY_SPACE, hold=25, repeat=4) and world.current_alg == "A_Star":
        astar_update(world.start_node, world.target_node)

    if pyxel.btnp(pyxel.KEY_RETURN) and world.current_alg == "A_Star":
        while world.heap:
            astar_update(world.start_node, world.target_node)

    world.player_pos = px,py
    if x != 0:
        world.player_dir = 1 if x > 0 else -1
    world.player_state = "Moving" if x != 0 or y != 0 else "Idle"

def draw_ui():
    draw9s(0, 128, 0, 56, 128, 32, 8, 12, 0)

    if world.current_alg == "A_Star":
        lib.text_shadow(pyxel.width - 54, ui_y, "Selected: A*", 7, 0)
    if world.current_alg == "DFS":
        lib.text_shadow(pyxel.width - 54, ui_y, "Selected: DFS", 7, 0)
    if world.current_alg == "BFS":
        lib.text_shadow(pyxel.width - 54, ui_y, "Selected: BFS", 7, 0)

    hover = get_node_at(*get_tile_coord(pyxel.mouse_x,pyxel.mouse_y))
    if hover and hover.h < 9000 and hover.g < 9000:
        t = int(hover.h + hover.g)
        lib.text_shadow(5, ui_y, f"G: {int(hover.g)}\nH: {int(hover.h)}\nT: {t}", 7, 0)
    else:
        lib.text_shadow(5, ui_y, f"G: -\nH: -\nT: -", 7, 0)


    lib.text_shadow(pyxel.width - 75, pyxel.height - 8, "Press '?' for help", 7, 0)
    if world.help_ui_active:
        draw9s(5, 5, 0, 40, pyxel.width - 10, pyxel.height - 42, 8, 12, 8)
        help_txt = """
Controls:

WASD         Move character
Num 1-3      Select alg

For A*:

SPACE [TAP]  Search node
SPACE [HOLD] Auto search
RETURN       Finish search
        """
        lib.text_shadow(10, 10, help_txt, 7, 0)


def draw():
    pyxel.bltm(0,0,0,0,0,128,128)

    px, py = world.player_pos
    side = 0 if world.player_dir == -1 else 8
    anim = pyxel.frame_count % 16 // 8 * 8 if world.player_state == "Moving" else 0
    pyxel.blt(px, py, 0, side, anim, 8, 8, 0)

    for n in map_graph:
        if n == world.start_node:
            continue
        if world.target_node:
            pyxel.rect(*get_node_pos(world.target_node), 2, 2, 6)
        if n and n.processed:
            pyxel.rect(*get_node_pos(n), 2, 2, 8)
        elif n and n.visited:
            pyxel.rect(*get_node_pos(n), 2, 2, 3)

    for n in world.path:
        pyxel.rect(n.index[1]*8+4, n.index[0]*8+4, 2, 2, 7)


    draw_ui()

    color = pyxel.pget(pyxel.mouse_x, pyxel.mouse_y)
    pyxel.blt(pyxel.mouse_x + - 3, pyxel.mouse_y - 3, 0, 0, 16, 8, 8, 0)

player_speed = 1.2
world = World()
g_cost = 10
ui_y = 135

pyxel.init(128,160, title="Pathfinding", fps=60, display_scale=5)
pyxel.load("Assets/pathfinding.pyxres")
map_graph = generate_graph()
# debug_print_graph()
world.player_pos = pyxel.width // 2 - 12, pyxel.height // 2 - 12
pyxel.run(update, draw)
