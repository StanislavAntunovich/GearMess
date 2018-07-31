from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib


def make_password(salt, password):
    bpassword = password.encode('UTF-8')
    pass_hex = hashlib.pbkdf2_hmac('sha256', bpassword, salt, 150000)
    passw = b64encode(pass_hex).decode('utf-8')
    return passw


def crypt_message(key, message, iv=None):
    key_ = b64decode(key)
    crypter = AES.new(key_, AES.MODE_CBC, iv=iv)
    iv = b64encode(crypter.iv).decode('utf-8')
    ct = b64encode(crypter.encrypt(pad(message.encode('UTF-8'), AES.block_size))).decode('utf-8')
    return iv + ct


def decrypt_message(key, message):
    key_ = b64decode(key)
    iv = b64decode(message[:24])
    word = b64decode(message[24:])
    crypter = AES.new(key_, AES.MODE_CBC, iv=iv)
    res = unpad(crypter.decrypt(word), AES.block_size)
    return res.decode('UTF-8')


def check_word(key, word_to_check, origin_word):
    iv = b64decode(word_to_check[:24])
    crypted_word = crypt_message(key, origin_word, iv)
    return True if crypted_word == word_to_check else False
