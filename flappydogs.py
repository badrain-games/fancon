import pyxel

player_x = 60
jump_boost = 2.6
gravity = 0.228
fork_separation = 60
fork_speed = 2

class App:
    def __init__(self):
        pyxel.init(250,160, title="Flappy Dogs")
        pyxel.load("Assets/flappydogs.pyxres")

        self.player_y = 30
        self.player_dy = jump_boost
        self.is_dead = False
        self.forks = [(i * fork_separation + pyxel.width, 30) for i in range(1, 6)]

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

        for i,(x,y) in enumerate(self.forks):
            self.forks[i] = (x - fork_speed, y)


    def draw(self):
        pyxel.cls(12)
        pyxel.blt(player_x, self.player_y, 0, 0, 32, 16, 16, 0)
        # pyxel.blt(playerX + 20, 0, 0, 0, 48, 16, 32, 0)
        for fork in self.forks:
            pyxel.blt(fork[0], fork[1], 0, 0, 80, 16, 16, 0)
        pyxel.text(5, 5, "Flappy Dogs", 1)
        pyxel.text(5, 10, f"{self.player_y}", 1)

App()
