import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        self.die = pg.mixer.Sound('sounds/smb_mariodie.wav')
        self.jump = pg.mixer.Sound('sounds/smb_jump-small.wav')
        self.stomp = pg.mixer.Sound('sounds/smb_stomp.wav')
        self.bump = pg.mixer.Sound('sounds/smb_bump.wav')
        self.powerup = pg.mixer.Sound('sounds/smb_powerup.wav')
        self.end_theme = pg.mixer.Sound('sounds/smb_gameover.wav')

    def play_music(self, music, volume=0.3):
        pg.mixer.music.unload()
        pg.mixer.music.load(music)
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.play(-1, 0.0)

    def busy(self):
        return pg.mixer.get_busy()

    def play_sound(self, sound):
        pg.mixer.Sound.play(sound)

    def play_bg(self):
        #self.play_music('sounds/smb_theme.mp3')
        pass

    def play_fast_bg(self):
        self.play_music('sounds/smb_hurry.mp3')

    def play_game_over(self):
        self.stop_bg()
        self.play_sound(self.end_theme)
        while self.busy():
            pass

    def stop_bg(self): pg.mixer.music.stop()

    def play_jump(self):
        self.play_sound(self.jump)

    def play_mario_dies(self):
        pg.mixer.stop()
        self.play_sound(self.die)
        while self.busy():
            pass



