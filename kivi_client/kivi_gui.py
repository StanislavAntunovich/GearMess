from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button


class SManager(ScreenManager):

    def ok_pressed(self, login, password, action):
        if login and password:
            pass
        else:
            # TODO: добавить кнопку 'OK'
            pop = Popup(
                title='Something not filled', content=(Label(text='Please fill all fields')),
                size_hint=(0.4, 0.4), auto_dismiss=True
            )
            pop.open()


class GearMessApp(App):

    def build(self):
        Window.size = (410, 500)
        return SManager()


if __name__ == '__main__':
    GearMessApp().run()
