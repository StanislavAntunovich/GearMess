from PyQt5 import QtCore, QtWidgets, uic
import sys

from ui.MyGuiWidgets import MessageBoxes
from JIM.jim_config import *


class LoginWindow(QtWidgets.QDialog):
    ok_button_signal = QtCore.pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('ui/ui_files/welcomeSecondWidget.ui', self)

        self.okPushButton.clicked.connect(self.ok_button_clicked)
        self.cancelPushButton.clicked.connect(self.close)

    def ok_button_clicked(self):
        login = self.loginLineEdit.text()
        password = self.passwordLineEdit.text()
        if login and password:
            self.ok_button_signal.emit(AUTHORISE, login, password)
            self.passwordLineEdit.clear()
        else:
            self.parent().info_boxes('info', 'not enough info', 'please fill all fields')
