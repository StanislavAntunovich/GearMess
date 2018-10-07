from sqlalchemy import Column, Integer, String, Text, BLOB
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class UserContacts(Model):
    __tablename__ = 'contacts'
    contact_id = Column(Integer, primary_key=True, autoincrement=True)
    contact_name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.contact_name = name


class IgnoreList(Model):
    __tablename__ = 'ignore_list'
    id = Column(Integer, primary_key=True)
    contact_name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.contact_name = name


class MessagesHistory(Model):
    __tablename__ = 'messages_history'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    from_contact = Column(String, nullable=True)
    to_contact = Column(String, nullable=True)
    message = Column(Text)
    message_created = Column(String)

    # contact = relationship('UserContacts', back_populates='messages')

    def __init__(self, message, from_contact=None, to_contact=None, message_created=None):
        self.message = message
        self.from_contact = from_contact
        self.to_contact = to_contact
        if message_created:
            self.message_created = str(message_created)


#TODO: добавить больше персональной информации
class PersonalInfo(Model):
    __tablename__ = 'personal_info'
    login = Column(String, primary_key=True)
    email = Column(String, nullable=True)
    photo = Column(BLOB, nullable=True)

    def __init__(self, login, email=None, photo=None):
        self.login = login
        self.email = email
        self.photo = photo
