from pymongo import MongoClient

client = MongoClient()
data_base = client.client_db

contacts_collection = data_base.user_contacts
messages_history_collection = data_base.messages_history
