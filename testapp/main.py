import os
import sys
import json

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.properties import StringProperty


class MainWindow(Widget):
    filename = StringProperty(sys.argv[1])

    def play_sound(self):
        if getattr(sys, 'frozen', False):
            os.environ['GST_PLUGIN_PATH'] = os.path.join(sys._MEIPASS, 'gst-plugins')

        print(json.dumps(dict(os.environ), indent=4, sort_keys=True))

        sound = SoundLoader.load(self.filename)
        sound.play()

class TestApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    TestApp().run()
