from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window

class GameWorld(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Sini nanti kita masukkan inisialisasi Joystick/Player
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        # Logika pergerakan player.move() pindah ke sini
        pass

class MagicalForestApp(App):
    def build(self):
        return GameWorld()

if __name__ == '__main__':
    MagicalForestApp().run()
