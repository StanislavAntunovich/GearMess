from pymongo import MongoClient

client = MongoClient()
data_base = client.server_db

users_collection = data_base.users
users_collection.create_index('user', unique=True)

messages_history_collection = data_base.messages_history
