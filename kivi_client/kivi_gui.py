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
from time import ctime, sleep

from client_src.client import Client
from JIM.jim_config import *


class SManager(ScreenManager):
    main_action = StringProperty(None)
    messages = ListProperty()
    chat_with = StringProperty()
    contacts = ObjectProperty()
    adapter = ListAdapter(data=[], cls=ListItemButton, selection_mode='single')

    MESSAGE_DRAW_PATTERN = '{}; FROM: {}, : {}'

    client = None
    service_queue = Queue()

    on_line = False

    def _receive(self):
        while self.on_line:
            message = self.client.receive()
            if message:
                if message.get(MESSAGE):
                    if self.chat_with == message[FROM]:
                        self.messages.append(
                            self.MESSAGE_DRAW_PATTERN.format(message[TIME], message[FROM], message[MESSAGE])
                        )
                else:
                    self.service_queue.put(message)

    def make_client(self, name, password):
        if not (name and password):
            pop = Popup(
                title='Something not filled', content=(Label(text='Please fill all fields')),
                size_hint=(0.5, 0.9), auto_dismiss=True
            )
            pop.open()
        else:
            self.client = Client(name)
            try:
                if self.main_action == 'Login':
                    resp = self.client.send_authorisation(password)
                else:
                    resp = self.client.send_registration(password)
            except WindowsError:
                Popup(
                    title='Error', content=(Label(text='No connection')),
                    size_hint=(0.5, 0.9), auto_dismiss=True
                ).open()
            else:
                if resp.get(RESPONSE) == OK:
                    self.current = 'main_screen'
                    self.on_line = True
                    Thread(target=self._receive).start()
                    sleep(0.2)
                    self.client.send_presence()
                    self.make_adapter()
                    self.get_contacts()
                elif resp.get(ERROR):
                    Popup(
                        title='Error', content=(Label(text='{}'.format(resp[ERROR]))),
                        size_hint=(0.5, 0.5), auto_dismiss=True
                    ).open()

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
                Popup(
                    title='Error', content=(Label(text='{}'.format(resp[ERROR]))),
                    size_hint=(0.5, 0.5), auto_dismiss=True
                ).open()

    def del_contact(self):
        name = self.chat_with
        if name != '#all':
            self.client.del_contact(name)
            resp = self.service_queue.get()
            if resp.get(RESPONSE) == OK:
                self.contacts.adapter.data.remove(name)
                self.contacts._trigger_reset_populate()
            else:
                Popup(
                    title='Error', content=(Label(text='{}'.format(resp[ERROR]))),
                    size_hint=(0.5, 0.5), auto_dismiss=True
                ).open()

    def get_contacts(self):
        self.client.get_contacts()
        contacts = self.service_queue.get()
        self.contacts.adapter.data.extend(contacts['contact_list'])

    def contact_changed(self, adapter):
        if adapter.selection:
            self.chat_with = adapter.selection[0].text

            if self.chat_with != '#all':
                self.messages = self._get_messages_history(self.chat_with)
        else:
            self.chat_with = '#all'

    def send_message(self, message):
        self.client.send_message(message, self.chat_with)
        self.messages.append(self.MESSAGE_DRAW_PATTERN.format(ctime(), self.client.name, message))

    def _get_messages_history(self, name):
        messages_list = []
        messages = self.client.get_messages_history(name)
        for message in messages:
            messages_list.append(self.MESSAGE_DRAW_PATTERN.format(message[TIME], message[FROM], message[MESSAGE]))
        return messages_list


class GearMessApp(App):

    def build(self):
        Window.size = (410, 500)
        return SManager()


if __name__ == '__main__':
    GearMessApp().run()
