import pyxel
import random


x = 10
y = 20
dx = 1
dy = 1
speed = 0.5
animate = True
size = 10

def update():
    global x, y, dx, dy, animate
    if x >= 128 - size:
        dx = -1
    if x <= 0:
        dx = 1
    if y >= 128 - size:
        dy = -1
    if y <= 0:
        dy = 1
        
    if pyxel.btnp(pyxel.KEY_T):
        animate = not animate
    
    if animate:
        x = x+dx*speed
        y = y+dy*speed

def draw():
    pyxel.cls(7)
    pyxel.rect(x, y, 10, 10, 0)

pyxel.init(128,128, title="Bouncing Ball", fps=120, display_scale=4)
pyxel.run(update, draw)

