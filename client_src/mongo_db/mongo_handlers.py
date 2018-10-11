from client_src.mongo_db.mongo_model import messages_history_collection, contacts_collection, ignore_list_collection


class UserContacts:
    def __init__(self):
        self.collection = contacts_collection

    def add_contact(self, name):
        self.collection.insert_one({'name': name})

    def del_contact(self, name):
        self.collection.delete_one({'name': name})


class MessagesHistory:
    def __init__(self):
        self.collection = messages_history_collection

    def log_message(self, json_message):
        self.collection.insert_one(json_message)

    def get_history(self, name):
        history = self.collection.find({'$or': [{'from': name}, {'to': name}]})
        return history


class IgnoreList:
    def __init__(self):
        self.collection = ignore_list_collection

    def add_to_ignore_list(self, name):
        self.collection.insert_one({'name': name})

    def is_ignored(self, name):
        checked = self.collection.find({'name': name})
        if checked:
            return True
        return False
