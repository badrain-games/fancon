import pyxel

player_x = 60
jump_boost = 1.93
gravity = 0.139
fork_speed = 1
fork_spawn_interval = 50
fork_spawn_count = 8
fork_midgap = 50

class App:
    def __init__(self):
        pyxel.init(250,160, title="Flappy Dogs", fps=60)
        pyxel.load("Assets/flappydogs.pyxres")

        self.player_y = 30
        self.player_dy = jump_boost
        self.is_dead = False
        self.forks = [(16 + pyxel.width, 30) for i in range(8)]
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
            self.forks[i] = (x_, y)


    def draw(self):
        pyxel.cls(12)
        # pyxel.blt(playerX + 20, 0, 0, 0, 48, 16, 32, 0)
        for fork_x,fork_y in self.forks:
            pyxel.blt(fork_x, fork_y, 0, 0, 80, 16, 16, 0)
            pyxel.blt(fork_x, fork_y + fork_midgap, 0, 0, 48, 16, 16, 0)
        pyxel.blt(player_x, self.player_y, 0, 0, 32, 16, 16, 0)
        pyxel.text(5, 5, "Flappy Dogs", 1)

App()
