from sqlalchemy.orm import *
from sqlalchemy import *

from GearMess.server_src.models import ClientContacts, Client, ClientsHistory, ClientsMessagesHistory
from GearMess.JIM.jim_config import *
from GearMess.JIM.JIMs import *

# TODO: убрать все респонсы от сюда, перенести их на сервер
# разбить на отдельные классы обработки контактов и истории подключений и сообщений

class StorageHandler:
    def __init__(self, session_):
        self.session = session_

    # def authorise(self, client_name):
    #     """ For now just checking if user registered or not, returns tuple to make relevant response
    #         :return: response and alert """
    #     if self.get_id_by_name(client_name):
    #         return
    #     else:
    #         return WRONG_LOGIN_INFO, WRONG_LOGIN_OR_PASSWORD

    def registration(self, client_name, password):
        """ For now just adding user in db (table Client)
            :return: response and alert """
        if not self.get_id_by_name(client_name):
            client = Client(client_name, password)
            self.session.add(client)
            self.session.commit()
            return OK, 'ok'
        else:
            return CONFLICT, ALREADY_EXISTS

    def count_contacts(self, client_name):
        """ Counting contacts by user-name 
            :return: quantity of contacts """
        quantity = self.session.query(ClientContacts).join(Client, ClientContacts.client_id == Client.id). \
            filter(Client.nick_name == client_name).count()
        return quantity

    def get_contacts(self, client_name):
        """ Finding contacts by user-name
            :return: list of contacts """
        cont_list = self.session.query(ClientContacts).join(Client, ClientContacts.client_id == Client.id). \
            filter(Client.nick_name == client_name).all()
        return [cont.contacts.nick_name for cont in cont_list]

    def get_id_by_name(self, contact_nickname):
        """ returns user id or None if user not existing """
        existing = self.session.query(Client).filter(Client.nick_name == contact_nickname).one_or_none()
        if existing:
            return existing.id
        else:
            return None

    def get_password(self, client_name):
        existing = self.session.query(Client).filter(Client.nick_name == client_name).one_or_none()
        return existing.password if existing else None

    def check_contact_in_list(self, client_name, contact_name):
        """ Checking if contact already in contact-list of user, if so - returns contact """
        client_id = self.get_id_by_name(client_name)
        contact_id = self.get_id_by_name(contact_name)
        contact = self.session.query(ClientContacts).filter(ClientContacts.client_id == client_id,
                                                            ClientContacts.contact_id == contact_id).one_or_none()
        return contact

    def add_contact(self, client_name, contact_name):
        """ Adding contact in user's contact-list, first checking if contact in db and not alreade in contact-list """
        if client_name == contact_name:
            return CONFLICT, TRYING_TO_ADD_SELF
        elif self.get_id_by_name(contact_name):
            client_id = self.get_id_by_name(client_name)
            contact_id = self.get_id_by_name(contact_name)
            if not self.check_contact_in_list(client_name, contact_name):
                contact = ClientContacts(client_id, contact_id)
                self.session.add(contact)
                self.session.commit()
                return OK, ADDED
            else:
                return CONFLICT, ALREADY_IN_LIST
        else:
            return NOT_FOUND, USER_NOT_EXISTS

    def del_contact(self, client_name, contact_name):
        """ Removeing contact from user's contact-list, first checking if contact is in list. """
        contact_to_del = self.check_contact_in_list(client_name, contact_name)
        if contact_to_del:
            self.session.delete(contact_to_del)
            self.session.commit()
            return OK, REMOVED
        else:
            return NOT_FOUND, CONTACT_NOT_IN_LIST

    def presence(self, client_name, ip_address):
        cl_id = self.get_id_by_name(client_name)
        if cl_id:
            log = ClientsHistory(cl_id, ip_address)
            self.session.add(log)
            self.session.commit()

    def log_message(self, sender, receiver, message, created=None):
        sender_id = self.get_id_by_name(sender)
        receiver_id = self.get_id_by_name(receiver)
        logged = ClientsMessagesHistory(sender_id, receiver_id, message, created)
        self.session.add(logged)
        self.session.commit()

    def get_messages_history(self, user):
        user_id = self.get_id_by_name(user)
        history = self.session.query(ClientsMessagesHistory).filter(or_(ClientsMessagesHistory.receiver_id==user_id,
                                                                        ClientsMessagesHistory.sender_id==user_id)).all()

