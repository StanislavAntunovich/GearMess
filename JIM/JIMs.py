import json
import time

from JIM.jim_config import *


class Jim:
    def __init__(self, name=None):
        self.name = name

    def _make_dict(self):
        return {}

    def create(self, **params):
        if ACTION in params:
            actions = JimAction(self.name)
            action = params.pop(ACTION)
            action_mess = actions.actions[action](**params)
            return action_mess
        elif RESPONSE in params:
            responser = JimResponse()
            return responser.make(**params)


class JimAction(Jim):
    def __init__(self, name=None):
        super().__init__(name)
        self.actions = {ADD_CONTACT: self.add_contact, DEL_CONTACT: self.del_contact, GET_CONTACTS: self.get_contacts,
                        AUTHORISE: self.authorise, REGISTER: self.register, MSG: self.message_to, QUIT: self.quit,
                        SYNC: self.sync, PRESENCE: self.presence, CONTACT_LIST: self.contact_list}

    def make(self, action, time_=None):
        message = super()._make_dict()
        if self.name:
            message[USER] = self.name
        message[ACTION] = action
        if not time_:
            message[TIME] = time.ctime()
        return message

    def presence(self):
        return self.make(PRESENCE)

    def add_contact(self, contact):
        message = self.make(ADD_CONTACT)
        message[CONTACT] = contact
        return message

    def del_contact(self, contact):
        message = self.make(DEL_CONTACT)
        message[CONTACT] = contact
        return message

    def get_contacts(self):
        return self.make(GET_CONTACTS)

    def contact_list(self, quantity, contact_list):
        message = self.make(CONTACT_LIST)
        message[QUANTITY] = str(quantity)
        message[CONTACT_LIST] = contact_list
        return message

    def authorise(self, answer=None):
        mess = self.make(AUTHORISE)
        if answer:
            mess[ANSWER] = answer
        return mess

    def register(self, password):
        mess = self.make(REGISTER)
        mess[PASSWORD] = password
        return mess

    def message_to(self, message, to='#all'):
        message_ = self.make(MSG)
        del (message_[USER])
        message_[FROM] = self.name
        message_[TO] = to
        message_[MESSAGE] = message
        return message_

    def quit(self):
        return self.make(QUIT)

    def sync(self):
        return self.make(SYNC)


class JimResponse(Jim):

    def make(self, response, alert=None):
        resp = super()._make_dict()
        resp[RESPONSE] = response
        resp[TIME] = time.ctime()
        if alert:
            if response.startswith(('4', '5')):
                resp[ERROR] = alert
            else:
                resp[ALERT] = alert
        return resp


class MessageConverter:
    """ Converting message. Taking code format on initialisation (UTF-8 is default)
        On call taking message as argument, checking message type and length of message parts.
        Choosing to encode or decode message.
        If message type not dict or bytes or  - rises TypeError"""

    def __init__(self, code_format='UTF-8'):
        self.LEN_LIMIT = {'action': 15, 'response': 3, 'name': 25, 'message': 500, 'time': 30, 'alert': 45}
        self.code_format = code_format

    def encoding(self, message):
        """ Encoding message: dict -> bytes.
            :param: message: dict-type message
            :return: bytes-type message"""
        smessage = json.dumps(message)
        return smessage.encode(self.code_format)

    def decoding(self, message):
        """ Decoding message: bytes -> dict...
            :param: message: bytes-type message
            :return: dict-type message"""
        smessage = message.decode(self.code_format)
        return json.loads(smessage)

    def check_len(self, message):
        """ Checking length of message parts.
            If part to long - rises TypeError.
            :param: message: dict-type message
            :raise: TypeError if some of items too long"""
        lens = message.keys()
        for item in lens:
            if self.LEN_LIMIT[item] < len(message[item]):
                raise TypeError('{} - text too long'.format(item))

    def __call__(self, message_to_convert):
        if isinstance(message_to_convert, dict):
            # self.check_len(message_to_convert)
            return self.encoding(message_to_convert)
        elif isinstance(message_to_convert, bytes):
            result = self.decoding(message_to_convert)
            # self.check_len(result)
            return result
        else:
            raise TypeError('{} unsupported argument format - {}'.format(message_to_convert, type(message_to_convert)))
