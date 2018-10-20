from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen


class SManager(ScreenManager):

    def join_pressed(self):
        pass

    def ok_pressed(self, login, password, action):
        print(login, '--', password, '==', action)


class GearMessApp(App):
    def build(self):
        return SManager()

if __name__ == '__main__':

    GearMessApp().run()
