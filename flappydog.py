import pyxel
import random

player_x = 60
sprite_size = 16
jump_boost = 2.55
gravity = 0.139
fork_speed = 1
tree_speed = 1
sploosh_speed = 0.5
fork_spawn_interval = 70
fork_spawn_count = 8
tree_spawn_count = 6
fork_midgap = 50
game_over_texts = ["Get Flopped!", "Get Forked!", "You're what's for dinner"]

def get_random_height():
    return random.randrange(20,90)

def get_random_gameover_text():
    return random.choice(game_over_texts)

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
        self.hit_vfx = (0, 0)
        self.player_state = "Start"
        self.last_anim = 0
        self.anim_time = 0
        self.vfx_anim_time = 0
        self.debug = False
        self.game_over_text = ""
        # pyxel.play(0, 5, loop = True)
        # pyxel.playm(0, loop = True)

        pyxel.run(self.update, self.draw)

    def reset(self):
        self.player_y = 30
        self.player_dy = 1
        self.score = 0
        self.player_state = "Playing"
        self.fork_spawn_idx = 0
        self.game_over_text = ""
        self.last_anim = 0
        self.anim_time = 0
        self.vfx_anim_time = 0

        for i in range(len(self.forks)):
            self.forks[i] = (-sprite_size, get_random_height(), True)

        for i in range(len(self.trees)):
            self.trees[i] = (i * 32, pyxel.height - 32)

    def handle_death(self, reason):
        self.game_over_text = get_random_gameover_text()
        self.player_state = reason
        self.hit_vfx = (player_x, self.player_y)

        if reason == "Dead_Crashed":
            pyxel.play(2, 1)

        elif reason == "Dead_Impaled":
            pyxel.play(2, 3)

    def start_update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.player_state = "Playing"

    def game_update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.player_dy = jump_boost
            self.sploosh_anims.append((player_x, self.player_y, pyxel.frame_count))
            pyxel.play(3, 0)


        self.player_dy -= gravity
        self.player_y -= self.player_dy

        if self.player_y + sprite_size >= pyxel.height:
            self.handle_death("Dead_Crashed")

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
                pyxel.play(2, 2)
            else:
                self.forks[i] = (x_, y, passed)

        # Collision Check
        for (x,y,passed) in self.forks:
            pright = player_x + sprite_size - 1
            shaftxl = player_x + 1 > x and player_x + 1 < x + sprite_size
            shaftxr = pright > x + 5 and pright < x + sprite_size - 5
            shaftyt = self.player_y + 5 < y
            shaftyb = self.player_y + sprite_size - 5 > y + fork_midgap + sprite_size
            forkxl = player_x + 1 > x + 1 and player_x + 1 < x + sprite_size - 1
            forkxr = pright > x and pright < x + sprite_size
            forkyt = self.player_y + 5 > y - 5 and self.player_y + 5 < y + sprite_size
            forkyb = (self.player_y + sprite_size - 5 > y + fork_midgap and
                      self.player_y + sprite_size - 5 < y + fork_midgap + sprite_size + 5)
            fork_collision = (forkxl or forkxr) and (forkyt or forkyb)
            shaft_collision = (shaftxl or shaftxr) and (shaftyt or shaftyb)
            if (fork_collision or shaft_collision):
                forky = y if forkyt else y + fork_midgap
                half = sprite_size // 2
                pcx,pcy = player_x + half, self.player_y + half
                fcx,fcy = x + half, forky + half
                distx = round(pcx - fcx)
                disty = round(pcy - fcy)
                dir = pyxel.atan2(distx, disty)
                print(dir)
                if ((dir > -35 and dir < 40) and forkyt) or ((dir < -140 or dir > 130) and forkyb):
                    self.handle_death("Dead_Impaled")
                else:
                    self.handle_death("Dead_Crashed")

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
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset()

        if self.player_state == "Dead_Crashed":
            if self.player_y < pyxel.height + sprite_size:
                self.player_dy -= gravity
                self.player_y -= self.player_dy
        elif self.player_state == "Dead_Impaled":
                if abs(self.player_dy) > 0.01:
                    self.player_dy *= 0.6
                    self.player_y -= self.player_dy

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.player_state == "Start":
            self.start_update()
        elif self.player_state == "Playing":
            self.game_update()
        elif self.player_state.startswith("Dead"):
            self.dead_update()


    def draw9s(self, x, y, u, v, w, h, cx, cy, tc):
        w2 = 16-cx
        h2 = 16-cy
        # TL Corner
        pyxel.blt(x, y, 0, u, v, cx, cy, tc)
        # TR Corner
        pyxel.blt(x + w - w2, y, 0, u + cx, v, w2, cy, tc)
        # BL Corner
        pyxel.blt(x, y + h - h2, 0, u, v + cy, cx, h2, tc)
        # BR Corner
        pyxel.blt(x + w - w2, y + h - h2, 0, u + cx, v + cy, w2, h2, tc)

        # Left Line
        for p in range(cx):
            color = pyxel.image(0).pget(u + p, v + cy-1)
            if color != tc:
                pyxel.line(x+p, y+cy, x+p, y+h-h2-1, color)
        # Top Line
        for p in range(cy):
            color = pyxel.image(0).pget(u+cx-1, v+p)
            if color != tc:
                pyxel.line(x+cx, y+p, x+w-w2-1, y+p, color)
        # Bottom Line
        for p in range(h2):
            color = pyxel.image(0).pget(u+cx-1, v+cy+p)
            if color != tc:
                pyxel.line(x+cx, y+h-h2+p, x+w-cx, y+h-h2+p, color)
        # Right Line
        for p in range(cx):
            color = pyxel.image(0).pget(u+cx+p, v+cy-1)
            if color != tc:
                pyxel.line(x+w+p-cx, y+cy, x+w+p-cx, y+h-h2-1, color)

        # Subtract cx and cy by 1 because the pixels are 0 indexed
        center_color = pyxel.image(0).pget(u + cx-1, v + cy-1)
        pyxel.rect(x+cx, y+cy, w-16, h-16, center_color)

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
            pyxel.blt(x, y, 0, animx, 80, sprite_size, sprite_size, 0)

        ff = lambda sploosh: ((pyxel.frame_count - sploosh[2]) // anim_speed) < 4
        self.sploosh_anims = list(filter(ff, self.sploosh_anims))


        if self.player_state == "Playing":
            u = sprite_size if self.player_dy > 0 else 0
            pyxel.blt(player_x, self.player_y, 0, u, 32, sprite_size, sprite_size, 0)

        # Draw Start Screen
        if self.player_state == "Start":
            self.draw9s(33, 60, 0, 112, 92, 16, 8, 12, 8)
            # Text Outline
            pyxel.text(38, 66, "Press Space to start!", 0)
            pyxel.text(38, 65, "Press Space to start!", 7)

        # Draw Game Over
        if self.player_state.startswith("Dead"):
            if self.player_state == "Dead_Impaled":

                if pyxel.frame_count % 100 == 0:
                    self.anim_time = 0

                anim_speed = 7
                if self.anim_time == anim_speed:
                    self.last_anim = 16
                elif self.anim_time == anim_speed * 2:
                    self.last_anim = 0
                elif self.anim_time == anim_speed * 3:
                    self.last_anim = 16
                elif self.anim_time == anim_speed * 4:
                    self.last_anim = 0

                self.anim_time += 1
                pyxel.blt(player_x, self.player_y, 0, self.last_anim, 32, sprite_size, sprite_size, 0)
            else:
                pyxel.blt(player_x, self.player_y, 0, 0, 32, sprite_size, sprite_size, 0)

            sprite_u = 64 + (16 * (self.vfx_anim_time // 4))
            self.vfx_anim_time += 1
            if sprite_u <= 112:
                pyxel.blt(self.hit_vfx[0], self.hit_vfx[1], 0, sprite_u, 88, 16, 16, 0)

            text_width = (len(self.game_over_text) * 4 + 10)
            self.draw9s((pyxel.width / 2) - (text_width / 2), 60, 0, 112, text_width, 16, 8, 12, 8)
            # Text Outline
            pyxel.text((pyxel.width / 2) - (text_width / 2) + 5, 66, self.game_over_text, 0)
            pyxel.text((pyxel.width / 2) - (text_width / 2) + 5, 65, self.game_over_text, 7)

            self.draw9s(45, 130, 0, 112, 73, 16, 8, 12, 8)
            # Text Outline
            pyxel.text(50, 136, "Press R to reset", 0)
            pyxel.text(50, 135, "Press R to reset", 7)

        # Draw score backplate
        self.draw9s(0, 0, 0, 112, 45, 16, 8, 12, 8)

        # Text Outline
        pyxel.text(5, 6, f"Score {self.score}", 0)
        pyxel.text(5, 5, f"Score {self.score}", 7)
        if self.debug:
            pyxel.text(5, 15, str(self.player_y), 1)
            pyxel.text(5, 35, f"Anims {len(self.sploosh_anims)}", 8)


App()
