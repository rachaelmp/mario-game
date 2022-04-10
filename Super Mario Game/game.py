import pygame as pg
from sys import exit
from time import sleep
from stats import Stats
from sound import Sound
from sprites import *
from settings import *
from os import path


class Game:
    def __init__(self):
        pg.init()
        self.stats = Stats(game=self)
        self.sound = Sound()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.finished = False
        self.font_name = pg.font.match_font(FONT)
        self.load()

    def load(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'images')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new_game(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerup = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.player = Mario(self)

        for platform in PLATFORM_LIST:
            Platform(self, *platform)

        for block in BLOCK_LIST:
            Block(self, *block)

        self.play()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.collision()

        if self.stats.lives_left < 1:
            self.finished = True
        if self.stats.time_left < 1:
            self.finished = True

    def collision(self):
        # check if player hits a platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                highest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                    if hit.rect.bottom < highest.rect.bottom:
                        highest = hit
                # if self.player.pos.x < lowest.rect.right + 15 * SCALE
                # and self.player.pos.x > lowest.rect.left - 15 * SCALE:
                if self.player.pos.y < lowest.rect.centery:
                    if self.player.vel.y > 0:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        # checks collision in the y axis
        self.player.rect.bottom -= 30
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        self.player.rect.bottom += 30
        if hits:
            left = hits[0]
            for hit in hits:
                if hit.rect.left > left.rect.left:
                    left = hit
            right = hits[0]
            for hit in hits:
                if hit.rect.right > left.rect.right:
                    left = hit
            if self.player.vel.x > 0:
                self.player.pos.x = left.rect.left - 7.5 * SCALE
                # hits[0].rect.left - hits[0].rect.width / 4
            if self.player.vel.x < 0:
                self.player.pos.x = right.rect.right + 7.5 * SCALE
                # hits[0].rect.right + hits[0].rect.width / 4

    def check_events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.finished = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                if event.key == pg.K_w:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump_cut()
                if event.key == pg.K_w:
                    self.player.jump_cut()

        if self.player.rect.right >= WIDTH / 2 and self.player.vel.x > 0:
            self.player.pos.x += -self.player.vel.x
            for play in self.platforms:
                play.rect.right += -self.player.vel.x

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw_bg(self):
        self.screen.fill(BG_COLOR)
        self.background_img = pg.image.load(f'images/level_bg.png').convert_alpha()
        self.background_rect = self.background_img.get_rect()
        self.background_img = pg.transform.scale(self.background_img, (self.background_rect.width * SCALE,
                                                                  self.background_rect.height * SCALE))
        self.background_rect = self.background_img.get_rect()

        self.level = pg.Surface((self.background_rect.width, self.background_rect.height)).convert()
        self.level_rect = self.level.get_rect()

        self.screen.blit(self.background_img, (0, 0))

    def draw_scoreboard(self):
        self.draw_text(str('SCORE'), 22, WHITE, 20 * SCALE, 10 * SCALE)
        self.draw_text(str('COINS'), 22, WHITE, 60 * SCALE, 10 * SCALE)
        self.draw_text(str('TIME'), 22, WHITE, 100 * SCALE, 10 * SCALE)
        self.draw_text(str('LIVES'), 22, WHITE, 140 * SCALE, 10 * SCALE)
        self.draw_text(str('HIGH SCORE'), 22, WHITE, 200 * SCALE, 10 * SCALE)

        self.draw_text(str(self.stats.score), 22, WHITE, 20 * SCALE, 20 * SCALE)
        self.draw_text(str(self.stats.coins), 22, WHITE, 60 * SCALE, 20 * SCALE)
        self.draw_text(str(self.stats.time_left), 22, WHITE, 100 * SCALE, 20 * SCALE)
        self.draw_text(str(self.stats.lives_left), 22, WHITE, 140 * SCALE, 20 * SCALE)
        self.draw_text(str(self.stats.high_score), 22, WHITE, 200 * SCALE, 20 * SCALE)

    def draw(self):
        # Game Loop - draw

        self.draw_bg()
        self.all_sprites.draw(self.screen)
        self.draw_scoreboard()
        pg.display.flip()

    def bgm(self):
        self.sound.play_bg()

    def play(self):
        self.bgm()
        while not self.finished:
            self.clock.tick(FPS)
            self.update()
            self.draw()
            self.check_events()

        self.game_over()
        sleep(0.5)

    def game_over(self):
        print('\nGAME OVER!\n')
        self.screen.fill(BLACK)
        self.draw_text(str('GAME OVER'), 22, WHITE, 128 * SCALE, 120 * SCALE)
        pg.display.flip()
        self.sound.play_game_over()

def main():
    g = Game()
    g.new_game()


if __name__ == '__main__':
    main()
