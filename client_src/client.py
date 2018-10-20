import socket
from time import sleep

from JIM.JIMs import Jim, MessageConverter
from JIM.jim_config import *
from client_src.client_storage_handler import ClientStorageHandler
from crypto.crypto import *

BUF_SIZE = 6000



class Client:
    def __init__(self, name, host, port, buff_size):
        self.name = name
        self.address = host, port
        self.buff_size = buff_size
        self.soc = None
        # TODO: при регистрации генерировать соль и записывать в базу или файл
        self.salt = b'e690a758702ee2f78e4ae5d1327f52d246c82a6eda3648d25c3806142717e5d3'
        self.message_key = '40tisachobezianvzhopusunulibanan'  # (с) С.Лукьяненко - Лабиринт Отражений.
        self.message_maker = Jim(self.name)
        self.converter = MessageConverter()
        self.storage_handler = ClientStorageHandler(self.name)

    def connect_to_server(self):
        """ Making socket and connecting to server_src"""
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.address)
        self.soc.settimeout(1)

    # TODO: поубирать receive из авторизации и регистрации -> перенести в welcomeWindow -> разбить методы
    def send_authorisation(self, password):
        """ Sending authorisation-message to server_src, returns received response """
        self.connect_to_server()
        authorisation_ = self.message_maker.create(action=AUTHORISE)
        authorisation = self.converter(authorisation_)
        self.soc.send(authorisation)

        serv_answ = self.receive()[ALERT]

        key = make_password(self.salt, password)
        answ = crypt_message(key, serv_answ)

        answer = self.message_maker.create(action=ANSWER, answer=answ)
        answer = self.converter(answer)
        self.soc.send(answer)
        resp = self.receive()
        return resp

    def send_registration(self, password):
        """ Sending registration-message to server_src, returns received response """
        passw = make_password(self.salt, password)
        self.connect_to_server()
        registration = self.message_maker.create(action=REGISTER, password=passw)
        registration = self.converter(registration)
        self.soc.send(registration)
        resp = self.receive()
        return resp

    def add_contact(self, contact_name):
        """ Sending action-message with contact name to add """
        action = self.message_maker.create(action=ADD_CONTACT, contact=contact_name)
        action = self.converter(action)
        self.soc.send(action)
        self.storage_handler.add_contact(contact_name)

    def del_contact(self, contact_name):
        """ Sending action-message with contact name to delete, returns received response """
        action = self.message_maker.create(action=DEL_CONTACT, contact=contact_name)
        action = self.converter(action)
        self.soc.send(action)
        self.storage_handler.del_contact(contact_name)

    def get_contacts(self):
        """ Sending action-message to get contact-list, printing contacts received from server_src """
        action = self.message_maker.create(action=GET_CONTACTS)
        action = self.converter(action)
        self.soc.send(action)

    def quit_server(self):
        quit_msg = self.message_maker.create(action=QUIT)
        quit_msg = self.converter(quit_msg)
        self.soc.send(quit_msg)
        sleep(0.2)
        self.soc.close()

    def send_presence(self):
        msg = self.message_maker.create(action=PRESENCE)
        msg = self.converter(msg)
        self.soc.send(msg)
        self.soc.settimeout(0.1)

    def receive(self):
        """ Receiving message from server_src, checking for message-action,
         if so - returns  string in format SENDER'S_NAME: MESSAGE."""
        try:
            mess = self.soc.recv(self.buff_size)
        except socket.timeout:
            pass
        else:
            if mess:
                dmess = self.converter(mess)
                if dmess.get(MESSAGE):
                    encrypted_message = decrypt_message(self.message_key, dmess[MESSAGE])
                    dmess[MESSAGE] = encrypted_message
                    self.storage_handler.log_incoming_message(dmess)
                return dmess

    def log_message(self, message):
        self.storage_handler.log_incoming_message(message[MESSAGE])

    def send_message(self, message, to):
        """ Making dict message-action and sending to server_src
        """
        message_ = self.message_maker.create(action=MSG, message=message, to=to)
        self.storage_handler.log_outgoing_message(message_)
        crypted_message = crypt_message(self.message_key, message)
        message_[MESSAGE] = crypted_message
        message_to_send = self.converter(message_)
        self.soc.send(message_to_send)

    def get_messages_history(self, contact_name):
        return self.storage_handler.messages_history(contact_name)

    def set_personal_info(self, login, email=None, photo=None):
        self.storage_handler.add_personal_info(login, email, photo)



