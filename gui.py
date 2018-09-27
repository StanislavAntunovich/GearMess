from PyQt5 import QtCore, QtGui, QtWidgets, uic
from queue import Queue

import time
import sys

from JIM.jim_config import *
from client_src.client import Client
from ui.main_window import Ui_MainWindow

from ui.MyGuiWidgets import EmojiListWidget, MessageBoxes

SELF_MESSAGES_COLOR = 'gray'
OTHER_MESSAGES_COLOR = 'black'

HTML_MESSAGE_PATTERN = '<span style=" color: {}"; >{} - {}: {}</span><br>'


class Receiver(QtCore.QThread):
    new_message_signal = QtCore.pyqtSignal(dict)

    def __init__(self, service_queue, user, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.service_queue = service_queue
        self.on_line = False
        self.user = user

    def run(self):
        self.on_line = True
        while self.on_line:
            message = self.parent().user.receive()
            if message:
                if message.get(MESSAGE):
                    self.new_message_signal.emit(message)
                else:
                    self.service_queue.put(message)


class WelcomeWidget(QtWidgets.QWidget):
    login_button_signal = QtCore.pyqtSignal()
    join_button_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('ui/welcomeFirstWidget.ui', self)

        self.loginPushButton.clicked.connect(self.login_button_signal.emit)
        self.joinPushButton.clicked.connect(self.join_button_signal.emit)

    def on_cancelPushButton_clicked(self):
        sys.exit(-1)


class LoginDataWidget(QtWidgets.QWidget):
    ok_button_signal = QtCore.pyqtSignal(str, str, str)
    cancel_button_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('ui/welcomeSecondWidget.ui', self)

        self.action = None

        self.message_boxes = MessageBoxes(self)

        self.okPushButton.clicked.connect(self.ok_button_clicked)
        self.cancelPushButton.clicked.connect(self.cancel_button_signal.emit)

    def ok_button_clicked(self):
        login = self.loginLineEdit.text()
        password = self.passwordLineEdit.text()
        if login and password:
            self.ok_button_signal.emit(self.action, login, password)
            self.passwordLineEdit.clear()
        else:
            self.message_boxes('info', 'not enough info', 'please fill all fields')


class LoginWindow(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        QtWidgets.QStackedWidget.__init__(self, parent)
        self.resize(231, 332)

        self.login_data_window = LoginDataWidget(self)
        self.welcome_window = WelcomeWidget(self)

        self.addWidget(self.login_data_window)
        self.addWidget(self.welcome_window)
        self.setCurrentWidget(self.welcome_window)

        self.welcome_window.login_button_signal.connect(lambda: self.login_data_widget(AUTHORISE))
        self.welcome_window.join_button_signal.connect(lambda: self.login_data_widget(REGISTER))

        self.login_data_window.cancel_button_signal.connect(self.login_data_window_cancel_clicked)

    def login_data_widget(self, action):
        self.resize(349, 276)
        self.setCurrentWidget(self.login_data_window)
        self.login_data_window.action = action

    def login_data_window_cancel_clicked(self):
        self.resize(231, 332)
        self.setCurrentWidget(self.welcome_window)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, user, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.user = user
        self.chat_with = '#all'

        self.service_queue = Queue()
        self.receiver = Receiver(self.service_queue, self.user, self)
        self.receiver.new_message_signal.connect(self.incoming_messages)

        self.infoBoxes = MessageBoxes(self)

        self.contactsListWidget.itemDoubleClicked.connect(self.contacts_list_double_click)
        self.contactsListWidget.add_contact_signal.connect(self.add_contact)
        self.contactsListWidget.del_contact_signal.connect(self.del_contact)

        self.addContactPushButton.clicked.connect(self.add_contact)
        self.deleteContactPushButton.clicked.connect(self.del_contact)
        self.addNonContactPushButton.clicked.connect(self.contactsListWidget.context_add_contact)

        self.messageSendTextEdit.send_message_signal.connect(self.outgoing_message)
        self.sendMessagePushButton.clicked.connect(self.outgoing_message)

        self.contactsListWidget.itemSelectionChanged.connect(self.set_buttons_box)

        self.emojiButton.clicked.connect(self.emoji_button_clicked)
        self.emojiWidget = EmojiListWidget(parent=self.emojiButton, emoji_dir_path='./ui/emoji/')
        self.emojiWidget.emojiClicked.connect(self.emoji_clicked)

        self.on_start()

    def emoji_clicked(self, emoji_html):
        self.messageSendTextEdit.insertHtml(emoji_html)

    def emoji_button_clicked(self):
        if self.emojiWidget.isVisible():
            self.emojiWidget.hide()
            self.messageSendTextEdit.setFocus()
        else:
            self.emojiWidget.show()

    def set_contacts_count_label(self, count=None):
        contacts_count = self.contactsListWidget.count() if not count else count
        self.ContactsCountLabel.setText('Total: '.format(contacts_count))

    def set_chat_with_label(self, name):
        pattern = 'Chat With: {}'.format(name)
        self.chatTextLabel.setText(pattern)

    def contacts_list_double_click(self):
        self.chat_with = self.contactsListWidget.currentItem().text()
        self.set_chat_with_label(self.chat_with)
        messages_history = self.user.get_messages_history(self.chat_with)
        self.ChatBrowser.clear()
        self.incoming_messages(messages_history)
        self.contactsListWidget.item_double_clicked()
        self.messageSendTextEdit.setFocus()

    def set_user_name(self, name):
        self.userNameLabel.setText(name)

    def outgoing_message(self, message=None):
        message_to_send = self.messageSendTextEdit.toHtml() if not message else message
        message_to_ins = HTML_MESSAGE_PATTERN.format(SELF_MESSAGES_COLOR, time.ctime(), self.user.name, message_to_send)
        self.ChatBrowser.insertHtml(message_to_ins)
        self.ChatBrowser.ensureCursorVisible()
        self.user.send_message(message_to_send, self.chat_with)
        self.messageSendTextEdit.clear()

    def incoming_messages(self, messages):
        if isinstance(messages, dict):
            self.incoming_message(messages)
        elif isinstance(messages, list):
            for message in messages:
                self.incoming_message(message)

    def incoming_message(self, message):
        colors = {self.user.name: SELF_MESSAGES_COLOR, self.chat_with: OTHER_MESSAGES_COLOR}
        if message.get(FROM) in (self.user.name, self.chat_with):
            color = colors[message[FROM]]
            message_to_ins = HTML_MESSAGE_PATTERN.format(color, message[TIME], message[FROM], message[MESSAGE])
            self.ChatBrowser.insertHtml(message_to_ins)
            self.ChatBrowser.ensureCursorVisible()
        else:
            self.contactsListWidget.new_message(message[FROM])

    def set_buttons_box(self):
        if self.contactsListWidget.currentItem().in_contacts:
            self.contactsActionsBox.setCurrentWidget(self.contactsWidget)
        else:
            self.contactsActionsBox.setCurrentWidget(self.nonContactsWidget)

    def get_contacts(self):
        self.user.get_contacts()
        contact_list = self.service_queue.get()
        self.contactsListWidget.add_contacts(contact_list[CONTACT_LIST])
        self.set_contacts_count_label()

    def add_contact(self, contact=None):
        contact_to_add = self.addContactLineEdit.text() if not contact else contact
        if contact_to_add:
            self.user.add_contact(contact_to_add)
            response = self.service_queue.get()
            if response.get(RESPONSE) == OK:
                self.contactsListWidget.add_contact(contact_to_add)
                self.addContactLineEdit.clear()
            else:
                self.infoBoxes(ERROR, ERROR, response[ERROR])
        else:
            self.infoBoxes('info', 'not filled', 'please fill contact name')

    def del_contact(self, contact=None):
        contact_to_del = self.contactsListWidget.currentItem().text() if not contact else contact
        self.user.del_contact(contact_to_del)
        response = self.service_queue.get()
        if response.get(RESPONSE) == OK:
            self.contactsListWidget.takeItem(self.contactsListWidget.currentRow())
        else:
            self.infoBoxes(ERROR, ERROR, response[ERROR])

    def closeEvent(self, event):
        self.receiver.on_line = False
        self.hide()
        self.receiver.wait(500)
        self.user.quit_server()
        event.accept()

    def on_start(self):
        self.receiver.start()
        self.get_contacts()
        self.user.send_presence()
        self.set_user_name(self.user.name)


class ClientGui:
    def __init__(self):
        self.loginWindow = LoginWindow()
        self.info_boxes = MessageBoxes()
        self.loginWindow.login_data_window.ok_button_signal.connect(self.ok_clicked)

        self.loginWindow.show()

    def ok_clicked(self, action, login, password):
        user = Client(login)
        if action == REGISTER:
            response = user.send_registration(password)
        else:
            response = user.send_authorisation(password)

        if response.get(RESPONSE) == OK:
            self.loginWindow.close()
            del self.loginWindow
            self.mainWindow = MainWindow(user)
            self.mainWindow.show()
        elif response.get(ERROR):
            self.info_boxes('error', 'error', response[ERROR])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ClientGui()
    sys.exit(app.exec_())
