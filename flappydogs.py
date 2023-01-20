import pyxel

class App:
    def __init__(self):
        pyxel.init(250,160, title="Flappy Dogs")
        pyxel.load("Assets/flappydogs.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(12)
        pyxel.blt(pyxel.width // 2, pyxel.height // 2, 0, 0, 32, 16, 16, 0)
        pyxel.text(5, 5, "Flappy Dogs", 1)

App()
