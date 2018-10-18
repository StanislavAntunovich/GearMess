from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class MyWidget(ScreenManager):
    def on_pr(self):
        self.current = 'login'

    def ok_p(self):
        print(self.ids.name.text)
        self.ids.name.select_all()
        self.ids.name.cut()


class AnchorLayout1(AnchorLayout):
    Window.size = (310, 290)

    def on_pr(self):
        print(self.size)


class SomeApp(App):
    def build(self):
        return MyWidget()


SomeApp().run()
