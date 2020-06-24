from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

class Spaceship(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    score = NumericProperty(0)
    pausescore = NumericProperty(0)
    current_highscore = NumericProperty(0)
    soundscore = NumericProperty(1)
    with open('highscore.txt', 'r') as f:
        highscore = f.read()

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class SpaceGame(Widget):
    player = ObjectProperty(None)
    stones = ObjectProperty(None)
    restartpos = ObjectProperty(None)
    playbuttonpos = ObjectProperty(None)
    highscorepos = ObjectProperty(None)
    pausepos = ObjectProperty(None)
    playpos = ObjectProperty(None)
    currenthighscorepos = ObjectProperty(None)
    soundscorepos = ObjectProperty(None)

    def serve_ball(self):
        self.player.velocity = Vector(0, 0)
        self.stones.velocity = Vector(0, 0)

    def restart_game(self):
        self.stones.x = randint(0, Window.width - self.stones.width)
        self.stones.y = Window.height
        self.player.x = Window.width / 2 - self.player.width / 2
        self.player.score = 0
        self.restartpos.x = Window.width + Window.width
        self.restartpos.y = Window.height + Window.height
        self.playbuttonpos.x = 0
        self.playbuttonpos.y = 0
        self.player.velocity = Vector(0, 0)
        self.stones.velocity = Vector(0, 0)
        self.highscorepos.x = Window.width / 2 - self.highscorepos.width / 2
        self.highscorepos.y = Window.height - self.highscorepos.height - self.highscorepos.height
        self.soundscorepos.x = Window.width - self.soundscorepos.width


    def update(self, dt):
        self.player.move()
        self.stones.move()

        if (self.player.x < 0) or (self.player.x > Window.width - self.player.width):
            self.player.velocity_x *= -1

        if (self.stones.y < 0):
            self.stones.x = randint(0, Window.width - self.stones.width)
            self.stones.y = Window.height
            self.player.score += 10

        if self.player.score == 100:
            self.stones.velocity_y = -6

        if self.player.score == 500:
            self.stones.velocity_y = -8

        if self.player.score == 2000:
            self.stones.velocity_y = -10

        if self.stones.collide_widget(self.player):
            with open('highscore.txt', 'w') as f:
                f.write(str(self.player.highscore))

            if self.player.score > int(self.player.highscore):
                self.player.highscore = self.player.score
                self.remove_widget(self.highscorepos)
                self.currenthighscorepos.x = Window.width / 2 - self.currenthighscorepos.width / 2
                self.currenthighscorepos.y = Window.height - self.currenthighscorepos.height - self.currenthighscorepos.height

            if self.player.score > self.player.current_highscore:
                self.player.current_highscore = self.player.score

            self.player.velocity = Vector(0, 0)
            self.stones.velocity = Vector(0, 0)
            self.restartpos.x = Window.width / 2 - self.restartpos.width / 2
            self.restartpos.y = Window.height / 3
            self.pausepos.x = Window.width + Window.width
            self.pausepos.y = Window.height + Window.height

    def moveship(self):
        if (self.player.x <= 0) or (self.player.x >= Window.width - self.player.width):
            self.player.velocity_x *= 1

        else:
            self.player.velocity_x *= -1
            if self.player.soundscore == 1:
                self.sound = SoundLoader.load('swap.wav')
                self.sound.play()

    def startgame(self):
        self.player.velocity = Vector(5, 0)
        self.stones.velocity = Vector(0, -5)
        self.playbuttonpos.x = Window.height + Window.height
        self.playbuttonpos.y = Window.width + Window.width
        self.highscorepos.x = Window.height + Window.height
        self.highscorepos.y = Window.width + Window.width
        self.pausepos.x = 0
        self.pausepos.y = Window.height - self.pausepos.height
        self.soundscorepos.x = Window.width + Window.width

    def pause(self):
        self.stones.velocity = Vector(0, 0)
        self.playpos.x = 0
        self.playpos.y = Window.height - self.playpos.height
        self.pausepos.x = Window.width + Window.width
        self.pausepos.y = Window.height + Window.height
        if self.player.velocity_x < 0:
            self.player.pausescore = -1
            self.player.velocity = Vector(0, 0)
        if self.player.velocity_x > 0:
            self.player.pausescore = 1
            self.player.velocity = Vector(0, 0)

    def play(self):
        if self.player.score < 100:
            self.stones.velocity_y = -4

        if self.player.score > 100:
            self.stones.velocity_y = -6

        if self.player.score > 500:
            self.stones.velocity_y = -8

        if self.player.score > 2000:
            self.stones.velocity_y = -10

        if self.player.pausescore < 0:
            self.player.velocity_x = -5

        if self.player.pausescore > 0:
            self.player.velocity_x = 5

        self.playpos.x = 0
        self.playpos.y = Window.width + Window.width
        self.pausepos.x = 0
        self.pausepos.y = Window.height - self.pausepos.height

    def soundvolume(self):
        self.player.soundscore *= -1

class Stones(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class MyApp(App):
    def build(self):
        self.title = 'Dodge Tai'
        game = SpaceGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    MyApp().run()