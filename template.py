import pyxel
import pdb
import random
from dataclasses import dataclass

screen_width = 640
screen_height = 480

@dataclass
class World:
    pass

def update():
    pass

def draw():
    pyxel.cls(7)

pyxel.init(screen_width, screen_height, title="Title", fps=60, display_scale=2)
pyxel.run(update, draw)
