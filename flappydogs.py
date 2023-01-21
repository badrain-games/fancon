import pyxel

playerX = 60
jumpBoost = 2.6
gravity = 0.228

class App:
    def __init__(self):
        pyxel.init(250,160, title="Flappy Dogs")
        pyxel.load("Assets/flappydogs.pyxres")

        self.playerY = 30
        self.playerDy = jumpBoost
        self.isDead = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_SPACE):
            self.playerDy = jumpBoost

        self.playerDy -= gravity
        self.playerY -= self.playerDy

        if self.playerY > pyxel.height:
            self.isDead = True


    def draw(self):
        pyxel.cls(12)
        pyxel.blt(playerX, self.playerY, 0, 0, 32, 16, 16, 0)
        pyxel.text(5, 5, "Flappy Dogs", 1)
        pyxel.text(5, 10, f"{self.playerY}", 1)

App()
