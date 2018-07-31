"""Константы для jim протокола, настройки"""

ENCODING = 'utf-8'

# Ключи
ACTION = 'action'
RESPONSE = 'response'

ERROR = 'error'
ALERT = 'alert'

TIME = 'time'
TO = 'to'
FROM = 'from'
MESSAGE = 'message'
QUANTITY = 'quantity'


USER = 'user'
PASSWORD = 'password'
ANSWER = 'answer'
CONTACT = 'contact'

# Значения
PRESENCE = 'presence'
GET_CONTACTS = 'get_contacts'
ADD_CONTACT = 'add_contact'
DEL_CONTACT = 'del_contact'
AUTHORISE = 'authorise'
REGISTER = 'register'
MSG = 'msg'
QUIT = 'quit'
SYNC = 'synchronize'

UNKNOWN_ACTION = 'unknown_action'


# Коды ответов (будут дополняться)
BASIC_NOTICE = '100'
OK = '200'
CREATED = '201'
ACCEPTED = '202'

WRONG_REQUEST = '400'
NOT_AUTHORISED = '401'
WRONG_LOGIN_INFO = '402'
NOT_FOUND = '404'
CONFLICT = '409'

SERVER_ERROR = '500'

CONTACT_LIST = 'contact_list'
USER_NOT_EXISTS = 'user not exists'
ALREADY_EXISTS = 'user already exists'
TRYING_TO_ADD_SELF = 'trying to add self'
ALREADY_IN_LIST = 'contact already in contact-list'
CONTACT_NOT_IN_LIST = 'contact not in list'
ADDED = 'added'
REMOVED = 'removed'
WRONG_LOGIN_OR_PASSWORD = 'wrong login or password'


# Кортеж из кодов ответов
RESPONSE_CODES = (BASIC_NOTICE, OK, CREATED, ACCEPTED, WRONG_REQUEST, NOT_AUTHORISED, WRONG_LOGIN_INFO, NOT_FOUND,
                  CONFLICT, SERVER_ERROR)


# Кортеж действий
ACTIONS = (PRESENCE, MSG, GET_CONTACTS, ADD_CONTACT, DEL_CONTACT, REGISTER, AUTHORISE,  QUIT, SYNC)
