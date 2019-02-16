import os
import json

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.properties import StringProperty


class MainWindow(Widget):
    filename = StringProperty('enter full path to sound file')

    def play_sound(self):
        filename = self.filename.strip()
        if not os.path.exists(filename):
            print('file not found')
        sound = SoundLoader.load(filename)
        sound.play()

class TestApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    TestApp().run()
