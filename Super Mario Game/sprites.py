import pygame as pg
from settings import *
from sound import Sound
from stats import Stats
vec = pg.math.Vector2


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * SCALE, height * SCALE))
        image.convert_alpha()
        return image


class Mario(pg.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.sound = Sound()
        self.stats = Stats(game=self.game)
        self.walking = False
        self.jumping = False
        self.isRight = True
        self.running = False
        self.powered = False
        self.fire = False
        self.invincible = False
        self.dead = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_r
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 5.5, HEIGHT / 1.25)
        # self.pos = vec(WIDTH / 5.5, HEIGHT / 1.075)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_r = self.game.spritesheet.get_image(59, 0, 15, 15)
        self.standing_r.set_colorkey(BRIGHTPURPLE)
        self.standing_l = pg.transform.flip(self.standing_r, True, False)
        self.walk_frames_r = [self.game.spritesheet.get_image(59, 20, 15, 15),
                              self.game.spritesheet.get_image(59, 40, 15, 15),
                              self.game.spritesheet.get_image(59, 60, 15, 15)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BRIGHTPURPLE)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame_r = self.game.spritesheet.get_image(59, 100, 15, 15)
        self.jump_frame_r.set_colorkey(BRIGHTPURPLE)
        self.jump_frame_l = pg.transform.flip(self.jump_frame_r, True, False)
        self.turn_r = self.game.spritesheet.get_image(59, 80, 15, 15)
        self.turn_r.set_colorkey(BRIGHTPURPLE)
        self.turn_l = pg.transform.flip(self.turn_r, True, False)

        self.dying_frame = self.game.spritesheet.get_image(59, 240, 15, 15)
        self.dying_frame.set_colorkey(BRIGHTPURPLE)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 2 * SCALE
        self.rect.bottom += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2 * SCALE
        self.rect.bottom -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
        self.sound.play_jump()

    def update(self):
        self.animate()
        # jumping up slower than coming down

        if self.vel.y >= 0:
            self.acc = vec(0, PLAYER_GRAV)
        if self.vel.y < 0:
            self.acc = vec(0, PLAYER_GRAV * .4)

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACCELERATION
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACCELERATION
        if keys[pg.K_LSHIFT]:
            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACCELERATION * 5 / 3
            if keys[pg.K_a]:
                self.acc.x = -PLAYER_ACCELERATION * 5 / 3
            if keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACCELERATION * 5 / 3
            if keys[pg.K_d]:
                self.acc.x = PLAYER_ACCELERATION * 5 / 3

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        if not self.jumping:
            self.vel += self.acc
        # locks in jump animation to a certain extent
        if self.jumping:
            self.vel.y += self.acc.y
            self.vel.x += self.acc.x * .4
        if abs(self.vel.x) < 0.2:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # player hits left side of screen
        if self.pos.x < 0 + self.rect.width / 2:
            self.pos.x = 0 + self.rect.width / 2
        self.rect.midbottom = self.pos
        if self.pos.y > HEIGHT:
            self.dead = True
            self.image = self.dying_frame
            self.sound.play_mario_dies()
            self.stats.lives_left -= 1
            self.reset()

    def reset(self):
        self.pos = vec(WIDTH / 5.5, HEIGHT / 1.3)
        self.animate()
        self.dead = False

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            speed = 1;
            if self.running:
                speed = 5 / 3
            else:
                speed = 1
            if now - self.last_update > 75 / speed:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    if not self.jumping:  # lock in left and right when jumping to match game
                        self.isRight = True
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    if not self.jumping:
                        self.isRight = False
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if self.isRight:
                self.image = self.standing_r
            if not self.isRight:
                self.image = self.standing_l
        # show jumping animation
        if self.jumping:
            if self.isRight:
                self.image = self.jump_frame_r
            if not self.isRight:
                self.image = self.jump_frame_l


class Goomba(pg.sprite.Sprite):
    def __init__(self):
        pass


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, t):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [(self.game.spritesheet.get_image(180, 260, 15, 15)),  # ground
                  (self.game.spritesheet.get_image(180, 240, 15, 15)),  # brick
                  (self.game.spritesheet.get_image(200, 0, 32, 32)),  # small pipe]
                  (self.game.spritesheet.get_image(200, 55, 32, 16)),  # pipe body
                  (self.game.spritesheet.get_image(180, 180, 15, 15)),  # brick
                  ]
        self.image = images[t]
        self.image.set_colorkey(BRIGHTPURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y, t):
        self.groups = game.all_sprites, game.powerup
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [(self.game.spritesheet.get_image(180, 260, 15, 15)),  # ground
                  (self.game.spritesheet.get_image(180, 180, 15, 15)),  # brick
                  (self.game.spritesheet.get_image(200, 0, 32, 32)),  # small pipe]
                  (self.game.spritesheet.get_image(200, 55, 32, 16)),  # pipe body
                  (self.game.spritesheet.get_image(180, 240, 15, 15)),  # brick
                  ]
        self.image = images[t]
        self.image.set_colorkey(BRIGHTPURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        def update(self):
            pass


class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y, t):
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [(self.game.spritesheet.get_image(180, 120, 15, 15)),  # Question 1
                  (self.game.spritesheet.get_image(180, 140, 15, 15)),  # Question 2
                  (self.game.spritesheet.get_image(180, 160, 15, 15)),  # Question 3
                  (self.game.spritesheet.get_image(180, 220, 15, 15)),  # Question Empty
                  (self.game.spritesheet.get_image(180, 180, 15, 15)),  # brick
                  ]
        self.image = images[t]
        self.image.set_colorkey(BRIGHTPURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y