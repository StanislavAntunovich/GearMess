from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter

from queue import Queue
from threading import Thread

from client_src.client import Client
from JIM.jim_config import *


class SManager(ScreenManager):
    main_action = StringProperty(None)
    messages = ListProperty()
    chat_with = StringProperty()
    contacts = ObjectProperty()
    adapter = ListAdapter(data=[], cls=ListItemButton, selection_mode='single')

    client = None
    service_queue = Queue()

    on_line = False

    def _receive(self):
        while self.on_line:
            message = self.client.receive()
            if message:
                if message.get(MESSAGE):
                    # TODO: вывод на экран если в данный момент с этим общаемся
                    pass
                else:
                    self.service_queue.put(message)

    def make_client(self, name, password):
        if not (name and password):
            pop = Popup(
                title='Something not filled', content=(Label(text='Please fill all fields')),
                size_hint=(0.5, 0.5), auto_dismiss=True
            )
            pop.open()
        else:
            self.client = Client(name)
            if self.main_action == 'Login':
                print('login')
                self.client.send_authorisation(password)
            else:
                print('join')
                self.client.send_registration(password)
            self.current = 'main_screen'
            self.on_line = True
            Thread(target=self._receive).start()
            self.make_adapter()
            self.get_contacts()

    def make_adapter(self):
        self.adapter.bind(on_selection_change=self.contact_changed)
        self.contacts.adapter = self.adapter
        self.contacts.adapter.data.clear()

    def add_contact(self, name):
        if name:
            self.client.add_contact(name)
            resp = self.service_queue.get()
            if resp.get(RESPONSE) == OK:
                self.contacts.adapter.data.extend([name])
                self.contacts._trigger_reset_populate()
            else:
                # TODO: вывести popup с ошибкой
                pass

    def get_contacts(self):
        self.client.get_contacts()
        contacts = self.service_queue.get()
        self.contacts.adapter.data.extend(contacts['contact_list'])

    def contact_changed(self, adapter):
        self.chat_with = adapter.selection[0].text


class GearMessApp(App):

    def build(self):
        Window.size = (410, 500)
        return SManager()


if __name__ == '__main__':
    GearMessApp().run()
