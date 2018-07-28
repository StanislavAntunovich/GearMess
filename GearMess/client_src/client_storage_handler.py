from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_

from GearMess.client_src.client_models import *
from GearMess.JIM.jim_config import *


class ClientStorageHandler:
    def __init__(self, name, database=None):
        self.name = name
        self.pattern = 'sqlite:///{}.sqlite'.format(self.name)
        self.engine = create_engine(self.pattern)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self._create_db(self.engine)

    def _create_db(self, engine_):
        Model.metadata.create_all(bind=engine_)

    def check_in_list(self, contact_name):
        result = self.session.query(UserContacts).filter(UserContacts.contact_name == contact_name).one_or_none()
        if result:
            return result
        else:
            return None

    def get_name_by_id(self, contact_id):
        res = self.session.query(UserContacts).filter(UserContacts.contact_id == contact_id).one()
        return res.contact_name

    def add_contact(self, contact_name):
        contact = self.check_in_list(contact_name)
        if not contact:
            new_contact = UserContacts(contact_name)
            self.session.add(new_contact)
            self.session.commit()
        #     return True
        # else:
        #     return False

    def del_contact(self, contact_name):
        contact = self.check_in_list(contact_name)
        if contact:
            self.session.delete(contact)
            self.session.commit()
            return True
        else:
            return False

    def get_contacts(self):
        contact_list = self.session.query(UserContacts).all()
        return [contact.contact_name for contact in contact_list]

    def log_incoming_message(self, message):
        from_contact = message[FROM]
        message_to_log = MessagesHistory(message[MESSAGE], from_contact=from_contact, to_contact=None,
                                         message_created=message[TIME])
        self.session.add(message_to_log)
        self.session.commit()

    def log_outgoing_message(self, message):
        to_contact = message[TO]
        message_to_log = MessagesHistory(message[MESSAGE], from_contact=None, to_contact=to_contact,
                                         message_created=message[TIME])
        self.session.add(message_to_log)
        self.session.commit()

    # пока выгружает всю историю - добавить выгрузку по дням/ часам
    def messages_history(self, contact, counted_period=None, period='day'):
        messages_history = []
        messages = self.session.query(MessagesHistory).\
            filter(or_(MessagesHistory.from_contact == contact,
                       MessagesHistory.to_contact == contact)).all()
        for message_ in messages:
            if message_.from_contact:
                messages_history.append(
                    {TIME: message_.message_created, FROM: message_.from_contact,
                     MESSAGE: message_.message})
            else:
                messages_history.append(
                    {TIME: message_.message_created, FROM: self.name, MESSAGE: message_.message})
        return messages_history

    def sync(self, history_list):
        for message in history_list:
            pass

