from PyQt5 import QtWidgets, QtCore
import time

from queue import Queue

from JIM.jim_config import *

from ui.py_views.mainWindow import Ui_MainWindow
from ui.receiver import Receiver
from ui.MyGuiWidgets import MessageBoxes, EmojiListWidget

SELF_MESSAGES_COLOR = 'gray'
OTHER_MESSAGES_COLOR = 'black'

HTML_MESSAGE_PATTERN = '<span style=" color: {}"; >{} - {}: {}</span><br>'


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, user, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.user = user
        self.chat_with = '#all'

        self.service_queue = Queue()
        self.receiver = Receiver(self.service_queue, self.user, parent=self)
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
        self.trayIcon.show()

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
        if self.contactsListWidget.currentItem():
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
                self.set_buttons_box()
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

import sys
sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook
