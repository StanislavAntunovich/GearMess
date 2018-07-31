""" Kind of veeeery simple consoleUI for client """
from threading import Thread
from queue import Queue
from time import sleep

from GearMess.client_src.client import Client
from GearMess.JIM.jim_config import *
import sys


class ConsoleClient:
    def __init__(self):
        self.welcome_message = '\nДобро пожаловать в наш мессенджер\n'
        self.welcome_menu = '\n[1] - Регистрация \n' \
                            '[2] - Вход \n'

        self.help_menu = '\nlist\n' \
                         'add <имя контакта> - добавить контакт\n' \
                         'del <имя контакта> - удалить контакт\n' \
                         'to <имя контакта> <сообщение> - отправить адресное сообщение\n' \
                         'quit - выход\n'

        self.servise_queue = Queue()

        self.user = None
        self._online = False

    def registration(self, addr, port):
        name = input('Введите логин для регистрации: ')
        password = input('Введите пароль: ')
        self.user = Client(name)
        self.user.connect_to_server()
        answ = self.user.send_registration(password)
        return answ

    def authorisation(self, addr, port):
        name = input('Введите логин для входа: ')
        password = input('Введите пароль: ')
        self.user = Client(name)
        self.user.connect_to_server()
        answ = self.user.send_authorisation(password)
        return answ

    def get_contacts(self):
        self.user.get_contacts()
        contacts = self.servise_queue.get()
        for val, contact in enumerate(contacts['contact_list'], 1):
            print('{} - {}'.format(val, contact))

    def add_contact(self, name):
        self.user.add_contact(name)
        resp = self.servise_queue.get()
        if resp[RESPONSE] != OK:
            print(resp[ERROR])

    def del_contact(self, name):
        self.user.del_contact(name)
        resp = self.servise_queue.get()

        if resp[RESPONSE] != OK:
            print(resp[ERROR])

    def quit_(self):
        self.user.quit_server()
        sys.exit(1)

    def receive_messages(self):
        while self._online:
            message = self.user.receive()
            if message:
                if message.get(MESSAGE):
                    print('{}: from {} -> {}'.format(message[TIME], message[FROM], message[MESSAGE]))
                else:
                    self.servise_queue.put(message)

    def handle(self):
        while self._online:
            action = input('>: ')
            if action.startswith('add'):
                try:
                    name = action.split()[1]
                    print(f'name = {name}')
                except IndexError:
                    print('укажите имя контакта')
                else:
                    self.add_contact(name)
            elif action.startswith('del'):
                try:
                    name = action.split()[1]
                except IndexError:
                    print('укажите имя контакта')
                else:
                    self.del_contact(name)
            elif action.startswith('to'):
                try:
                    action = action.split()
                    name = action[1]
                    message = ' '.join(action[2:])
                except IndexError:
                    print('не задан получатель или текст сообщения')
                else:
                    self.user.send_message(message, name)
            elif action == 'list':
                self.get_contacts()
            elif action == 'quit':
                self.user.quit_server()
                self._online = False
                sleep(1)
                sys.exit(-1)
            else:
                print(self.help_menu)

    def welcome(self):
        # TODO: добавить обработку возможных ошибок ввода пользователя
        print(self.welcome_message)
        addr = input('Введите адрес сервера: ')
        port = int(input('Введите номер порта сервера: '))
        while True:
            print(self.welcome_menu)
            choise = input('Ваш выбор: ')
            if choise == '1':
                resp = self.registration(addr, port)
            elif choise == '2':
                resp = self.authorisation(addr, port)
                print(resp)
            else:
                resp = None
                print('Неверный выбор. \n 1 или 2, пожалуйста')

            if resp.get(RESPONSE) == '200':
                self._online = True
                self.user.send_presence()
                Thread(target=self.receive_messages).start()
                Thread(target=self.handle).start()
                break
            else:
                print(resp[ERROR])


if __name__ == '__main__':
    cli = ConsoleClient()
    cli.welcome()
