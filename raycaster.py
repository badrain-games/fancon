import pyxel as px
import random
import lib
import math
from dataclasses import dataclass

@dataclass
class World:
    player_pos = (0,0)
    player_dir = 0
    player_state = "Idle"
    map = [0] * 256

def is_boundary(x, y):
    _,ty = px.tilemap(0).pget(x // 8, y // 8)
    return ty == 0

def update():
    ()

colors = [2,3,4,8,9,10,12,13]
def draw():
    px.cls(6)
    for col in range(px.width):
        height = px.height * (0.3 + ((px.sin(col + px.frame_count) + 1) * 0.25))
        ch = (px.height - height) // 2
        px.line(col, ch, col, ch + height, colors[len(colors) - 1 - (((col+px.frame_count*2) // 6) % len(colors))])

px.init(640,400, title="Raycaster", fps=60, display_scale=2)
px.load("Assets/raycaster.pyxres")
world = World()

for row in range(16):
    for col in range(16):
        world.map[row * 16 + col] = 1 if is_boundary(col * 8, row * 8) else 0

px.run(update, draw)
