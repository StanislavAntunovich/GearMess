from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import datetime
import os

Base = declarative_base()


class Client(Base):
    __tablename__ = 'client_src'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nick_name = Column(String, unique=True)
    password = Column(String, nullable=False)
    info = Column(String, nullable=True)

    def __init__(self, name, password, info=None):
        self.nick_name = name
        self.password = password
        self.info = info


class ClientContacts(Base):
    __tablename__ = 'clients_contacts'
    client_id = Column(Integer, ForeignKey('client_src.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('client_src.id'), primary_key=True)

    clients = relationship('Client', foreign_keys=[client_id])
    contacts = relationship('Client', foreign_keys=[contact_id])

    def __init__(self, client_id, contact_id):
        self.client_id = client_id
        self.contact_id = contact_id


class ClientsHistory(Base):
    __tablename__ = 'clients_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client_src.id'))
    ip_address = Column(String)
    connected = Column(DATETIME, default=datetime.datetime.now())

    def __init__(self, client_id, ip_addr):
        self.client_id = client_id
        self.ip_address = ip_addr


class ChatRooms(Base):
    __tablename__ = 'chat_rooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String, unique=True)

    def __init__(self, room_name):
        self.room_name = room_name


class ClientsRooms(Base):
    __tablename__ = 'clients_rooms'
    client_id = Column(Integer, ForeignKey('client_src.id'), primary_key=True)
    room_id = Column(Integer, ForeignKey('chat_rooms.id'), primary_key=True)

    def __init__(self, client_id, room_id):
        self.client_id = client_id
        self.room_id = room_id


class ClientsMessagesHistory(Base):
    __tablename__ = 'messages_history'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('client_src.id'))
    receiver_id = Column(Integer, ForeignKey('client_src.id'))
    message = Column(Text)
    created = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, sender_id, receiver_id, message, created=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        if created:
            self.created = created


DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_FOLDER_PATH, '..\server.sqlite')
engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session = session
