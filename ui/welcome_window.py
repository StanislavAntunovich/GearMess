from PyQt5 import QtWidgets, QtCore, uic
import sys

from ui.join_window import JoinWindow
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.MyGuiWidgets import MessageBoxes

from JIM.jim_config import *
from client_src.client import Client


class WelcomeWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.info_boxes = MessageBoxes(self)

        self.login_window = LoginWindow(self)
        self.join_window = JoinWindow(self)
        self.main_window = None

        uic.loadUi('ui/ui_files/welcomeFirstWidget.ui', self)

        self.loginPushButton.clicked.connect(self.login_bttn_clicked)
        self.joinPushButton.clicked.connect(self.join_bttn_clicked)

        self.login_window.ok_button_signal.connect(self.make_client)
        self.join_window.ok_button_signal.connect(self.make_client)

    def login_bttn_clicked(self):
        self.login_window.show()

    def join_bttn_clicked(self):
        self.join_window.show()

    def on_cancelPushButton_clicked(self):
        sys.exit(-1)

    def make_client(self, action, login, password):
        user = Client(login)
        try:
            if action == REGISTER:
                response = user.send_registration(password)
            else:
                response = user.send_authorisation(password)
        except WindowsError:
            self.info_boxes('error', 'error', 'no connection to server')
        else:
            if response.get(RESPONSE) == OK:
                self.main_window = MainWindow(user)
                self.main_window.show()
                self.login_window.close()
                self.join_window.close()
                self.close()
            elif response.get(ERROR):
                self.info_boxes('error', 'error', response[ERROR])
