import pyxel
from pyxel import *
import pdb
import random

screenWidth = 512
screenHeight = 512

class Game:
    def __init__(self):
        pyxel.init(screenWidth,screenHeight, title="Game", fps=60, display_scale=2)

        self.pcount = 100
        self.immuneCount = 60
        self.immuneTime = 0
        self.gravity = 2
        self.ppos = []
        self.pvel = []
        self.pradius = []
        self.pmass = []
        self.pactive = []
        for i in range(self.pcount):
            self.pvel.append((0,0))
            self.ppos.append((rndi(2, screenWidth), rndi(2, screenHeight)))
            self.pradius.append(3)
            self.pmass.append(1)
            self.pactive.append(True)

        # pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.check = btn(KEY_D)
        if btnp(KEY_SPACE):
            if sum(self.pactive) == 1:
                self.immuneTime = self.immuneCount
                active = -1
                for i in range(self.pcount):
                    if self.pactive[i]:
                        active = i
                        break
                for i in range(self.pcount):
                    self.ppos[i] = self.ppos[active]
                    self.pradius[i] = 3
                    self.pmass[i] = 1
                    self.pactive[i] = True
                    v = 3.2
                    self.pvel[i] = random.uniform(-v, v), random.uniform(-v, v)

        if btnp(KEY_EQUALS):
            self.gravity += 0.5
        if btnp(KEY_MINUS):
            self.gravity -= 0.5


        if self.immuneTime <= 0:
            for i in range(self.pcount):
                if not self.pactive[i]:
                    continue
                for j in range(i+1, self.pcount):
                    if not self.pactive[j]:
                        continue
                    v1x, v1y, p1x, p1y, m1 = *self.pvel[i], *self.ppos[i], self.pmass[i]
                    v2x, v2y, p2x, p2y, m2 = *self.pvel[j], *self.ppos[j], self.pmass[j]
                    dx = p2x - p1x
                    dy = p2y - p1y
                    distSqr = dx**2 + dy**2
                    dist = sqrt(distSqr) * 2
                    # if dx == 0 and dy == 0:
                    #     dist = 0
                    #     force = 0
                    # else:
                    #     force = p1m * p2m / distSqr * 0.1
                    force = self.gravity * m1 * m2 / distSqr
                    ax = force * dx / dist
                    ay = force * dy / dist
                    self.pvel[i] = v1x + (ax / m1), v1y + (ay / m1)
                    self.pvel[j] = v2x - (ax / m2), v2y - (ay / m2)

        if self.immuneTime <= 0:
            for i in range(self.pcount):
                if not self.pactive[i]:
                    continue
                for j in range(i+1, self.pcount):
                    if not self.pactive[j]:
                        continue
                    p1x, p1y, p1r = *self.ppos[i], self.pradius[i]
                    p2x, p2y, p2r = *self.ppos[j], self.pradius[j]
                    dx = p2x - p1x
                    dy = p2y - p1y
                    if dx == 0 and dy == 0:
                        dist = 0
                    else:
                        dist = sqrt(dx**2 + dy**2)
                    if dist < p1r + p2r:
                        if p1r > p2r:
                            self.pactive[j] = False
                            self.pradius[i] += 2
                            self.pmass[i] += p2r * 2
                        elif p1r < p2r:
                            self.pactive[i] = False
                            self.pradius[j] += 2
                            self.pmass[j] += p1r * 2
                        else:
                            self.pactive[j] = False
                            self.pradius[i] += 2
                            self.pmass[i] += p2r * 2

        for i in range(self.pcount):
            if not self.pactive[i]:
                continue
            px, py, vx, vy, r = *self.ppos[i], *self.pvel[i], self.pradius[i]
            px,py = px + vx, py + vy

            if px + r > screenWidth:
                vx *= -1
                px = screenWidth - r
            if px - r < 0:
                vx *= -1
                px = r
            if py + r > screenHeight:
                vy *= -1
                py = screenHeight - r
            if py - r < 0:
                vy *= -1
                py = r

            ############
            # This commented out code is for screen wrapping but I
            # don't like it as much
            ############
            # if px - r > screenWidth:
            #     px = -r
            # if px + r < 0:
            #     px = screenWidth + r
            # if py - r > screenHeight:
            #     py = -r
            # if py + r < 0:
            #     py = screenHeight + r

            self.ppos[i] = px,py
            self.pvel[i] = vx,vy

        if self.immuneTime > 0:
            self.immuneTime -= 1

                ############
                # Leave this here in case you want to make billiard ball physics
                ############
                # dirx = x / dist
                # diry = y / dist
                # if dist < p1r + p2r:
                #     p1x, p1y = self.pvel[i]
                #     p2x, p2y = self.pvel[j]
                #     self.pvel[i] = p1x
                #     self.pvel[j] = self.pvel[j][0] * -1, self.pvel[j][1] * -1

    def draw(self):
        cls(7)

        for i in range(self.pcount):
            if not self.pactive[i]:
                continue
            circb(*self.ppos[i], self.pradius[i], 0)

g = Game()
