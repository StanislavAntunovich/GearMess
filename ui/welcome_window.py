from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

from ui.join_window import JoinWindow
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.MyGuiWidgets import MessageBoxes
from ui.py_views.welcomeWindow import Ui_welcomeFirstWidget

from JIM.jim_config import *
from client_src.client import Client


class WelcomeWidget(QtWidgets.QWidget, Ui_welcomeFirstWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.info_boxes = MessageBoxes(self)

        self.login_window = LoginWindow(self)
        self.join_window = JoinWindow(self)
        self.main_window = None

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

    def make_client(self, action, login, password, email=None, photo=None):
        user = Client(login)
        try:
            if action == REGISTER:
                response = user.send_registration(password)
            else:
                response = user.send_authorisation(password)
        except WindowsError as e:
            print(e)
            self.info_boxes('error', 'error', 'no connection to server')
        else:
            if response.get(RESPONSE) == OK:
                self.main_window = MainWindow(user)
                # user.set_personal_info(login, email, photo)
                self.main_window.show()
                self.login_window.close()
                self.join_window.close()
                self.close()
            elif response.get(ERROR):
                self.info_boxes('error', 'error', response[ERROR])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = WelcomeWidget()
    win.show()
    sys.exit(app.exec_())
