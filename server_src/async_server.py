import asyncio
from os import urandom
from time import sleep

from JIM.jim_config import *
from JIM.JIMs import *

from server_src.user_exceptions import *
from server_src.mongo_db.mongo_handlers import StorageHandler

from crypto.crypto import *


class ServerHandlerProtocol(asyncio.Protocol):
    def __init__(self, connections_, authorised_, online_):
        self.connections = connections_
        self.authorised_connections = authorised_
        self.online_connections = online_

        self.storage_handler = StorageHandler()
        self.converter = MessageConverter()
        self.message_maker = Jim()
        self.transport_auth_word = {}

    def connection_made(self, transport):
        self.transport = transport

    # TODO: понять как работает transport closed
    def connection_lost(self, exc):
        if isinstance(exc, ConnectionResetError):
            # client = self.connections.pop(self.transport)
            # del self.online_connections[client]
            self.authorised_connections.remove(self.transport)

    def data_received(self, data):
        if data:
            print(self.converter(data))
            self.message_handle_router(data, self.transport)

    def message_handle_router(self, data, transport):
        message = self.converter(data)

        action = message.get(ACTION)
        resp = None
        if action != AUTHORISE and action != REGISTER and action != ANSWER:
            self.check_authorisation(transport)

        if action == MSG:
            self.income_message(message)
        elif action == PRESENCE:
            self.presence(message[USER], transport)
        elif action == GET_CONTACTS:
            resp = self.get_contacts(message[USER])
        elif action == ADD_CONTACT:
            resp = self.add_contact(message[USER], message[CONTACT])
        elif action == DEL_CONTACT:
            resp = self.del_contact(message[USER], message[CONTACT])

        elif action == AUTHORISE:
            self.authorise(transport, message[USER])
        elif action == ANSWER:
            resp = self.answer(message, transport)

        elif action == REGISTER:
            resp = self.registration(message[USER], message[PASSWORD], transport)
        elif action == QUIT:
            self.quit(message[USER])
        else:
            resp = self.unknown_action()
        if resp:
            response = self.converter(resp)
            transport.write(response)

    # TODO: доставка неотправленных сообщений
    def presence(self, user, transport):
        self.storage_handler.presence(user, transport.get_extra_info('sockname')[0])
        self.online_connections.update({user: transport})
        self.connections.update({transport: user})
        undelivered = self.storage_handler.get_undelivered(user)
        for message in undelivered:
            transport.write(self.converter(message))
            sleep(0.11)  # TODO: подумать как изменить, блокирует пока все не доставит

    def get_contacts(self, user):
        quantity = self.storage_handler.count_contacts(user)
        contact_list = self.storage_handler.get_contacts(user)
        resp_ = self.message_maker.create(
            action=CONTACT_LIST, quantity=quantity, contact_list=contact_list)
        return resp_

    def add_contact(self, user, contact):
        try:
            self.storage_handler.add_contact(user, contact)
        except ContactAlreadyInList:
            resp, alert = CONFLICT, ALREADY_IN_LIST
        except UserNotExisting:
            resp, alert = NOT_FOUND, USER_NOT_EXISTS
        except SelfAdding:
            resp, alert = CONFLICT, TRYING_TO_ADD_SELF
        else:
            resp, alert = OK, ADDED
        response = self.message_maker.create(response=resp, alert=alert)
        return response

    def del_contact(self, user, contact):
        try:
            self.storage_handler.del_contact(user, contact)
        except ContactNotInList:
            resp, alert = NOT_FOUND, CONTACT_NOT_IN_LIST
        else:
            resp, alert = OK, REMOVED
        response = self.message_maker.create(response=resp, alert=alert)
        return response

    # TODO: доработать - отправлять респ о том что юзер уже онлайн
    def authorise(self, transport, user):
        if user not in self.online_connections:
            self.transport_auth_word[transport] = b64encode(urandom(32)).decode('utf-8')
            request = self.message_maker.create(response=OK, alert=self.transport_auth_word[transport])
            request = self.converter(request)
            transport.write(request)
        else:
            transport.close()

    def answer(self, message, transport):
        answ = message[ANSWER]
        key = self.storage_handler.get_password(message[USER])
        if key and check_word(key, answ, self.transport_auth_word[transport]):
            resp_ = self.message_maker.create(response=OK, alert='authorised')
            self.authorised_connections.append(transport)
        else:
            resp_ = self.message_maker.create(response=WRONG_LOGIN_INFO, alert=WRONG_LOGIN_OR_PASSWORD)
        self.transport_auth_word.pop(transport)
        return resp_

    def quit(self, user):
        transport = self.online_connections.pop(user)
        del self.connections[transport]
        self.authorised_connections.remove(transport)
        transport.close()

    def unknown_action(self):
        resp = self.message_maker.create(response=WRONG_REQUEST, alert=UNKNOWN_ACTION)
        return resp

    # TODO: доставка сообщения если клиент не онлайн
    def income_message(self, message):
        if not message[TO].startswith('#'):
            if message[TO] in self.online_connections:
                recipient_transport = self.online_connections[message[TO]]
                recipient_transport.write(self.converter(message))
                self.storage_handler.log_message(message, delivered=True)
            else:
                self.storage_handler.log_message(message, delivered=False)
        else:
            for client in self.online_connections:
                self.online_connections[client].write(self.converter(message))

    def check_authorisation(self, transport):
        if transport in self.authorised_connections:
            return True
        else:
            resp = self.message_maker.create(response=NOT_AUTHORISED)
            resp = self.converter(resp)
            transport.write(resp)
            transport.close()
            return False

    def registration(self, user, password, transport):
        try:
            self.storage_handler.registration(user, password)
        except UserAlreadyExists:
            resp, alert = CONFLICT, ALREADY_EXISTS
        else:
            resp, alert = OK, ADDED
        response = self.message_maker.create(response=resp, alert=alert)
        self.authorised_connections.append(transport)
        return response
