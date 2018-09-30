""" Simple echo-server_src. Making socket. Forwarding messages from clients to every-listening.
        Takes ADDRESS and PORT to listen from on initialisation as required.
        Takes time_out=0.2, buf_size=2048, max_clients=15, code_format='UTF-8' as not required."""

from socket import socket, AF_INET, SOCK_STREAM, timeout
from os import urandom
from queue import Queue
from threading import Thread

from server_src.handlers import StorageHandler
from server_src.user_exceptions import *
from server_src.models import my_session

from JIM.JIMs import Jim, MessageConverter
from JIM.jim_config import *
from crypto.crypto import *


class Server:
    """ Simple echo-server_src. Making socket. Forwarding messages from clients to every-listening.
        Takes ADDRESS and PORT to listen from on initialisation as required.
        Takes time_out=0.2, buf_size=2048, max_clients=15, code_format='UTF-8' as not required"""

    def __init__(self, address, port_, time_out=0.2, buf_size=2048, max_clients=15, code_format='UTF-8'):
        """ :param address: address to listen from, :type: string, example '192.168.1.1'
            :param port_: port to listen from, :type: int, example 7777
        """
        self.addr = address, port_

        self.soc = None

        # через гуй добавить возможность отключать
        self._is_alive = False

        self.chats_messages = Queue()
        self.addressed_messages = Queue()

        self.connected_clients = []
        self.authorised_clients = []
        self.online_users = {}

        self.converter = MessageConverter()
        self.handler = ServerHandler(self.connected_clients, self.authorised_clients, self.online_users,
                                     self.addressed_messages, self.chats_messages)

        self._timeout = time_out
        self._buf_size = buf_size
        self._clients_count = max_clients
        self._code_format = code_format

        self.addressed_messages_thread = Thread(target=self.send_addressed_messages)
        self.chat_messages_thread = Thread(target=self.send_chat_messages)

    def listen(self):
        """ To make socket using initialised parameters"""
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.bind(self.addr)
        self.soc.settimeout(self._timeout)
        self.soc.listen(self._clients_count)

    def send_chat_messages(self):
        """ Method to use in thread to send chat-messages. """
        while self._is_alive:
            try:
                message = self.chats_messages.get()
            except:
                pass
            else:
                bmessage = self.converter(message)
                for user in self.online_users.values():
                    user.send(bmessage)

    def send_addressed_messages(self):
        """ To send addressed messages, tacking message from queue and sending it if user is on-line,
        if not - puts it back to queue"""
        while self._is_alive:
            try:
                message = self.addressed_messages.get()
            except:
                pass
            else:
                recipient = message[TO]
                conn = self.online_users.get(recipient)
                if conn:
                    message_ = self.converter(message)
                    conn.send(message_)
                else:
                    # TODO: в базу и ставить пометку не доставлено а при коннекте проверять есть ли не доставленные
                    # а то потеряются если сервер упадет
                    self.addressed_messages.put(message)

    def _accept(self):
        """ Handle every connected user. """
        try:
            conn, addr = self.soc.accept()
        except OSError:
            pass
        else:
            self.connected_clients.append(conn)
            Thread(target=self.handle_conn, args=(conn,)).start()

    def handle_conn(self, conn):
        """
        Using in thread to receive every request from certain user and initiate handling of each.
        :param conn: - socket of connected user :type: socket.
        """
        while conn in self.connected_clients:
            try:
                message = conn.recv(self._buf_size)
            except timeout:
                pass
            else:
                if message:
                    self.handler.handle(message, conn)


    def run(self):
        """ To start server_src working. """
        self._is_alive = True
        self.listen()
        self.addressed_messages_thread.start()
        self.chat_messages_thread.start()
        while True:
            self._accept()


class ServerHandler:
    def __init__(self, connected_clients, authorised_clients, online_users, addressed_messages, chat_messages):
        self.connected_clients = connected_clients
        self.authorised_clients = authorised_clients
        self.online_users = online_users

        self.chats_messages = chat_messages
        self.addressed_messages = addressed_messages

        self.storage_handler = StorageHandler(my_session)
        self.converter = MessageConverter()
        self.responder = Jim()

    def authorise(self, user, conn):
        word = b64encode(urandom(32)).decode('utf-8')
        request = self.responder.create(response=OK, alert=word)
        request = self.converter(request)
        conn.send(request)
        cl_answ = conn.recv(1024)
        cl_answ = self.converter(cl_answ)
        answ = cl_answ[ANSWER]
        key = self.storage_handler.get_password(user)
        if key and check_word(key, answ, word):
            resp_ = self.responder.create(response=OK, alert='authorised')
            self.authorised_clients.append(conn)
        else:
            resp_ = self.responder.create(response=WRONG_LOGIN_INFO, alert=WRONG_LOGIN_OR_PASSWORD)
        return resp_

    def registration(self, user, password, conn):
        try:
            self.storage_handler.registration(user, password)
        except UserAlreadyExists:
            resp, alert = CONFLICT, ALREADY_EXISTS
        else:
            resp, alert = OK, ADDED
        response = self.responder.create(response=resp, alert=alert)
        self.authorised_clients.append(conn)
        return response

    def check_authorisation(self, conn):
        if conn in self.authorised_clients:
            return True
        else:
            resp = self.responder.create(response=NOT_AUTHORISED)
            resp = self.converter(resp)
            conn.send(resp)
            # time.sleep(0.2)
            conn.close()
            return False

    def get_contacts(self, user):
        quantity = self.storage_handler.count_contacts(user)
        contact_list = self.storage_handler.get_contacts(user)
        resp_ = self.responder.create(action=CONTACT_LIST, quantity=quantity, contact_list=contact_list)
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
        response = self.responder.create(response=resp, alert=alert)
        return response

    def del_contact(self, user, contact):
        try:
            self.storage_handler.del_contact(user, contact)
        except ContactNotInList:
            resp, alert = NOT_FOUND, CONTACT_NOT_IN_LIST
        else:
            resp, alert = OK, REMOVED
        response = self.responder.create(response=resp, alert=alert)
        return response

    def presence(self, user, conn):
        self.storage_handler.presence(user, conn.getsockname()[0])
        self.online_users[user] = conn

    def unknown_action(self):
        resp = self.responder.create(response=WRONG_REQUEST, alert=UNKNOWN_ACTION)
        return resp

    def income_message(self, message):
        if message[TO].startswith('#'):
            self.chats_messages.put(message)
        else:
            self.addressed_messages.put(message)

    def quit(self, user):
        conn_ = self.online_users.pop(user)
        self.connected_clients.remove(conn_)
        self.authorised_clients.remove(conn_)
        conn_.close()

    def handle(self, message, conn):
        message = self.converter(message)
        action = message.get(ACTION)
        resp = None
        if action != AUTHORISE and action != REGISTER:
            self.check_authorisation(conn)

        if action == MSG:
            self.income_message(message)
        elif action == PRESENCE:
            self.presence(message[USER], conn)
        elif action == GET_CONTACTS:
            resp = self.get_contacts(message[USER])
        elif action == ADD_CONTACT:
            resp = self.add_contact(message[USER], message[CONTACT])
        elif action == DEL_CONTACT:
            resp = self.del_contact(message[USER], message[CONTACT])
        elif action == AUTHORISE:
            resp = self.authorise(message[USER], conn)
        elif action == REGISTER:
            resp = self.registration(message[USER], message[PASSWORD], conn)
        elif action == QUIT:
            self.quit(message[USER])
        else:
            resp = self.unknown_action()
        if resp:
            response = self.converter(resp)
            conn.send(response)


if __name__ == '__main__':
    server = Server('', 7777)
    server.run()
