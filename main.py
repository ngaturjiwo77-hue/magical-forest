from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
import math
import random

# --- CLASS PLAYER ---
class Player(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (60, 60)
        with self.canvas:
            Color(143/255, 240/255, 217/255, 1)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_canvas)

    def update_canvas(self, *args):
        self.ellipse.pos = self.pos

    def move(self, joystick_output_x, joystick_output_y):
        self.x += joystick_output_x * 10
        self.y += joystick_output_y * 10

# --- CLASS JOYSTICK ---
class VirtualJoystick(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_x = 0
        self.output_y = 0
        self.active = False
        with self.canvas:
            Color(1, 1, 1, 0.3)
            self.base = Ellipse(pos=self.pos, size=(200, 200))
            Color(143/255, 240/255, 217/255, 0.8)
            self.stick = Ellipse(pos=(self.x + 50, self.y + 50), size=(100, 100))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = True
            return True

    def on_touch_move(self, touch):
        if self.active:
            center_x, center_y = self.x + 100, self.y + 100
            dx = touch.x - center_x
            dy = touch.y - center_y
            dist = math.hypot(dx, dy)
            if dist > 100:
                angle = math.atan2(dy, dx)
                dx = math.cos(angle) * 100
                dy = math.sin(angle) * 100
            self.stick.pos = (center_x + dx - 50, center_y + dy - 50)
            self.output_x = dx / 100
            self.output_y = dy / 100

    def on_touch_up(self, touch):
        if self.active:
            self.active = False
            self.stick.pos = (self.x + 50, self.y + 50)
            self.output_x = 0
            self.output_y = 0

# --- CLASS UTAMA ---
class GameWorld(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(pos=(400, 400))
        self.joystick = VirtualJoystick(pos=(50, 50))
        self.add_widget(self.player)
        self.add_widget(self.joystick)
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        self.player.move(self.joystick.output_x, self.joystick.output_y)

class MagicalForestApp(App):
    def build(self):
        return GameWorld()

if __name__ == '__main__':
    MagicalForestApp().run()
