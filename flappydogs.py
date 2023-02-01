import pyxel
import random

player_x = 60
sprite_size = 16
jump_boost = 1.93
gravity = 0.139
fork_speed = 1
tree_speed = 1
sploosh_speed = 0.5
fork_spawn_interval = 70
fork_spawn_count = 8
tree_spawn_count = 6
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
        self.sploosh_anims = []
        self.player_state = "Playing"
        self.debug = False

        pyxel.run(self.update, self.draw)

    def reset(self):
        self.player_y = 30
        self.player_dy = 1
        self.score = 0
        self.player_state = "Playing"
        self.fork_spawn_idx = 0
        for i in range(len(self.forks)):
            self.forks[i] = (-sprite_size, get_random_height(), True)

        for i in range(len(self.trees)):
            self.trees[i] = (i * 32, pyxel.height - 32)

    def game_update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            self.player_dy = jump_boost

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.sploosh_anims.append((player_x, self.player_y, pyxel.frame_count))

        self.player_dy -= gravity
        self.player_y -= self.player_dy

        if self.player_y + sprite_size >= pyxel.height:
            self.player_state = "Dead_Crashed"

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

        # Collision Check
        for (x,y,passed) in self.forks:
            pright = player_x + sprite_size - 2
            colxl = player_x + 2 > x and player_x + 2 < x + sprite_size
            colxr = pright > x and pright < x + sprite_size
            colyt = self.player_y + 5 < y + sprite_size
            colyb = self.player_y + sprite_size - 5 > y + fork_midgap
            if ((colxl or colxr) and (colyt or colyb)):
                forky = y if colyt else y + fork_midgap
                half = sprite_size // 2
                pcx,pcy = player_x + half, self.player_y + half
                fcx,fcy = x + half, forky + half
                distx = round(pcx - fcx)
                disty = round(pcy - fcy)
                dir = pyxel.atan2(distx, disty)
                print(dir)
                if ((dir > -35 and dir < 40) and colyt) or ((dir < -140 or dir > 120) and colyb):
                    self.player_state = "Dead_Impaled"
                else:
                    self.player_state = "Dead_Crashed"

        # Loop trees
        if pyxel.frame_count % 2 == 0:
            for i,(x, y) in enumerate (self.trees):
                x_ = x - tree_speed
                if x_ <= -32:
                    # When wrapping around from index 0 to 5, we update the
                    # x positions out of order so we need to predict index 5's
                    # position by adding the tree_speed
                    wrap_around = tree_speed if i == 0 else 0
                    x_ = self.trees[(i - 1) % tree_spawn_count][0] + 32 - wrap_around

                self.trees[i] = (x_, y)

        for i,(x,y,fc) in enumerate(self.sploosh_anims):
            self.sploosh_anims[i] = x - sploosh_speed,y,fc

    def dead_update(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

        if self.player_state == "Dead_Crashed":
            if self.player_y < pyxel.height + sprite_size:
                self.player_dy -= gravity
                self.player_y -= self.player_dy
        # elif self.player_state == "Dead_Impaled":
            # if self.player_y < pyxel.height + sprite_size:
            #     self.player_y += 0.1

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.player_state == "Playing":
            self.game_update()
        elif self.player_state.startswith("Dead"):
            self.dead_update()

    def draw9s(self):
        cwidth = 110
        cheight = 120
        offset = 25
        # TL
        pyxel.blt(offset, offset, 0, 0, 112, 8, 8, 8)
        # TR
        pyxel.blt(cwidth + offset, offset, 0, 8, 112, 8, 8, 8)
        # BL
        pyxel.blt(offset, cheight + offset, 0, 0, 120, 8, 8, 8)
        # BR
        pyxel.blt(cwidth + offset, cheight + offset, 0, 8, 120, 8, 8, 8)

        # Top Line
        pyxel.line(offset + 8, offset + 1, cwidth + offset, offset + 1, 7)

        # Vertical Rect
        pyxel.rect(offset + 8, offset + 2, cwidth - 8, cheight + 4, 1)


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
            pyxel.blt(fork_x, fork_y, 0, 0, 48, sprite_size, -sprite_size, 0)

            pyxel.blt(fork_x, fork_y + fork_midgap, 0, 0, 48, sprite_size, sprite_size, 0)
            for i in range(6):
                pyxel.blt(fork_x, fork_y + fork_midgap + (sprite_size * (i + 1)), 0, 0, 64, sprite_size, sprite_size, 0)

        anim_speed = 5
        # Draw hotdog animation
        for x,y,fc in self.sploosh_anims:
            animx = ((pyxel.frame_count - fc) // anim_speed) * sprite_size
            pyxel.blt(x, y, 0, animx, 96, sprite_size, sprite_size, 0)

        ff = lambda sploosh: ((pyxel.frame_count - sploosh[2]) // anim_speed) < 4
        self.sploosh_anims = list(filter(ff, self.sploosh_anims))


        u = sprite_size if self.player_dy > 0 else 0
        pyxel.blt(player_x, self.player_y, 0, u, 32, sprite_size, sprite_size, 0)
        pyxel.text(5, 5, f"Score {self.score}", 1)
        if self.debug:
            pyxel.text(5, 15, str(self.player_y), 1)
            pyxel.text(5, 35, f"Anims {len(self.sploosh_anims)}", 8)

        self.draw9s()

App()
