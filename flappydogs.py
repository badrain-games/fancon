import pyxel
import random

player_x = 60
jump_boost = 1.93
gravity = 0.139
fork_speed = 1
fork_spawn_interval = 70
fork_spawn_count = 8
fork_midgap = 50

def get_random_height():
    return random.randrange(20,90)

class App:
    def __init__(self):
        pyxel.init(160,160, title="Flappy Dogs", fps=60)
        pyxel.load("Assets/flappydogs.pyxres")

        self.player_y = 30
        self.player_dy = jump_boost
        self.is_dead = False
        self.forks = [(-16, get_random_height()) for i in range(8)]
        self.fork_spawn_idx = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_SPACE):
            self.player_dy = jump_boost

        self.player_dy -= gravity
        self.player_y -= self.player_dy

        if self.player_y > pyxel.height:
            self.is_dead = True

        # Check if we need to spawn a new fork
        fork_spawn_reset = -1
        if pyxel.frame_count % fork_spawn_interval == 0:
            fork_spawn_reset = self.fork_spawn_idx
            self.fork_spawn_idx = (self.fork_spawn_idx + 1) % fork_spawn_count

        for i,(x,y) in enumerate(self.forks):
            x_ = x - fork_speed
            if fork_spawn_reset == i:
                x_ = pyxel.width + 16
                y = get_random_height()
            self.forks[i] = (x_, y)


    def draw(self):
        pyxel.cls(12)
        pyxel.blt(0, 0, 0, 16, 0, 32, 32)
        for fork_x,fork_y in self.forks:
            for i in range(6):
                pyxel.blt(fork_x, fork_y - (16 * (i + 1)), 0, 0, 64, 16, 16, 0)
            pyxel.blt(fork_x, fork_y, 0, 0, 80, 16, 16, 0)

            pyxel.blt(fork_x, fork_y + fork_midgap, 0, 0, 48, 16, 16, 0)
            for i in range(6):
                pyxel.blt(fork_x, fork_y + fork_midgap + (16 * (i + 1)), 0, 0, 64, 16, 16, 0)
        if self.player_dy < 0:
            pyxel.blt(player_x, self.player_y, 0, 0, 32, 16, 16, 0)
        else:
            pyxel.blt(player_x, self.player_y, 0, 16, 32, 16, 16, 0)
        pyxel.text(5, 5, "Flappy Dogs", 1)

App()
