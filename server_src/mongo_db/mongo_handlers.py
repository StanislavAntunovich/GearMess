from server_src.user_exceptions import *

from server_src.mongo_db.mongo_models import messages_history_collection, users_collection
from server_src.mongo_db.mongo_config import *


# TODO: добавить личную инфу и фото
class StorageHandler:
    def __init__(self):
        self.users = users_collection
        self.messages_history = messages_history_collection

    def registration(self, user, password):
        if self.user_existing(user):
            raise UserAlreadyExists(user)
        else:
            self.users.insert_one({USER: user, PASSWORD: password, CONTACTS: []})

    def add_contact(self, user, contact):
        if user == contact:
            raise SelfAdding(contact)
        if self.user_existing(contact):
            if not self.in_contacts(user, contact):
                self.users.update({USER: user}, {'$push': {CONTACTS: contact}})
            else:
                raise ContactAlreadyInList(contact)
        else:
            raise UserNotExisting(contact)

    def del_contact(self, user, contact):
        if self.in_contacts(user, contact):
            self.users.update({USER: user}, {'$pullAll': {CONTACTS: [contact]}})
        else:
            raise ContactNotInList(contact)

    def count_contacts(self, user):
        user_ = self.users.find_one({USER: user})
        return len(user_[CONTACTS])

    def get_contacts(self, user):
        return self.users.find_one({USER: user})[CONTACTS]

    def get_password(self, user):
        user_ = self.users.find_one({USER: user})
        if user_:
            return user_[PASSWORD]
        return None

    # TODO
    def presence(self, user, ip_address):
        pass

    def in_contacts(self, user, contact):
        if self.users.find_one({USER: user, CONTACTS: {'$in': [contact]}}):
            return True
        return False

    def user_existing(self, user):
        if self.users.find_one({USER: user}):
            return True
        return False

    def log_message(self, json_message, delivered=True):
        json_message.update({DELIVERED: delivered})
        self.messages_history.insert_one(json_message)

    def get_undelivered(self, user):
        messages_ = list(self.messages_history.find({'$and': [{TO: user}, {DELIVERED: False}]}))
        self.messages_history.update_many({'$and': [{TO: user}, {DELIVERED: False}]}, {'$set': {DELIVERED: True}})
        for message in messages_:
            message.pop('_id')
            message.pop(DELIVERED)
            yield message
        # return messages_


if __name__ == '__main__':
    messages_history_collection.drop()
    h = StorageHandler()
