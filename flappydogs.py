import pyxel
import random

player_x = 60
sprite_size = 16
jump_boost = 1.93
gravity = 0.139
fork_speed = 1
tree_speed = 1
fork_spawn_interval = 70
fork_spawn_count = 8
tree_spawn_count = 7
fork_midgap = 50

def get_random_height():
    return random.randrange(20,90)

class App:
    def __init__(self):
        pyxel.init(160,160, title="Flappy Dogs", fps=60)
        pyxel.load("Assets/flappydogs.pyxres")

        self.player_y = 30
        self.player_dy = 1
        self.score = 0
        self.forks = [(-sprite_size, get_random_height(), True) for i in range(fork_spawn_count)]
        self.fork_spawn_idx = 0
        self.trees = [(i * 32, pyxel.height - 32) for i in range(tree_spawn_count)]
        self.debug = False

        pyxel.run(self.update, self.draw)

    def reset(self):
        self.player_y = 30
        self.player_dy = 1
        self.score = 0
        self.fork_spawn_idx = 0
        for i in range(len(self.forks)):
            self.forks[i] = (-sprite_size, get_random_height(), True)

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

        for i,(x,y,passed) in enumerate(self.forks):
            x_ = x - fork_speed
            if fork_spawn_reset == i:
                x_ = pyxel.width + sprite_size
                y = get_random_height()
                passed = False
            if x_ + sprite_size < player_x and not passed:
                self.forks[i] = (x_, y, True)
                self.score += 1
            else:
                self.forks[i] = (x_, y, passed)


        for (x,y,passed) in self.forks:
            pright = player_x + sprite_size - 2
            player_height = sprite_size // 2
            if (((player_x + 2 > x and player_x + 2 < x + sprite_size)
                or (pright > x and pright < x + sprite_size))
                and (self.player_y + 5 < y + sprite_size or
                     self.player_y + sprite_size - 5 > y + fork_midgap)):
                self.reset()

        for i,(x, y) in enumerate (self.trees):
            x_ = x - tree_speed
            if x_ + 32 < player_x:
                self.trees[i] = (x_, y)


    def draw(self):
        pyxel.cls(12)
        pyxel.blt(0, 0, 1, 0, 0, 160, 160)

        #Draw Trees
        for tree_x, tree_y in self.trees:
            for i in range(tree_spawn_count):
                pyxel.blt(tree_x, tree_y, 0, 0, 0, 32, 32, 0)

        for fork_x,fork_y,passed in self.forks:
            for i in range(6):
                pyxel.blt(fork_x, fork_y - (sprite_size * (i + 1)), 0, 0, 64, sprite_size, sprite_size, 0)
            pyxel.blt(fork_x, fork_y, 0, 0, 80, sprite_size, sprite_size, 0)

            pyxel.blt(fork_x, fork_y + fork_midgap, 0, 0, 48, sprite_size, sprite_size, 0)
            for i in range(6):
                pyxel.blt(fork_x, fork_y + fork_midgap + (sprite_size * (i + 1)), 0, 0, 64, sprite_size, sprite_size, 0)



        u = sprite_size if self.player_dy > 0 else 0
        pyxel.blt(player_x, self.player_y, 0, u, 32, sprite_size, sprite_size, 0)
        pyxel.text(5, 5, f"Score {self.score}", 1)
        if self.debug:
            pyxel.text(5, 15, str(self.player_y), 1)
            pyxel.text(5, 25, f"Dead Count: {self.death_count}", 8)

App()
