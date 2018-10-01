# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.MyGuiWidgets import *

EMOJI_PATH = "ui/emoji/"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(997, 647)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # TODO: добавить меню, понять как убирать всплывшее сообщение, как открыть основое окно по клику на сообщение
        self.trayIcon = QtWidgets.QSystemTrayIcon()
        self.trayIcon.setIcon(QtGui.QIcon('ui/tray_icon/dsg.png'))

        self.ContactsCountLabel = QtWidgets.QLabel(self.centralwidget)
        self.ContactsCountLabel.setGeometry(QtCore.QRect(700, 110, 81, 20))
        self.ContactsCountLabel.setObjectName("ContactsCountLabel")
        self.contactsListWidget = MyListWidget(self.centralwidget)
        self.contactsListWidget.setGeometry(QtCore.QRect(700, 140, 261, 361))
        self.contactsListWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.contactsListWidget.setAcceptDrops(True)
        self.contactsListWidget.setObjectName("contactsListWidget")

        self.ChatBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.ChatBrowser.setGeometry(QtCore.QRect(30, 100, 641, 421))
        self.ChatBrowser.setObjectName("ChatBrowser")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ChatBrowser.setFont(font)
        self.addContactPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addContactPushButton.setGeometry(QtCore.QRect(890, 80, 61, 28))
        self.addContactPushButton.setObjectName("addContactPushButton")
        self.userNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.userNameLabel.setGeometry(QtCore.QRect(340, 10, 321, 20))
        self.userNameLabel.setTextFormat(QtCore.Qt.AutoText)
        self.userNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.userNameLabel.setObjectName("userNameLabel")
        self.chatTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.chatTextLabel.setGeometry(QtCore.QRect(40, 70, 251, 20))
        self.chatTextLabel.setObjectName("chatTextLabel")
        self.addContactLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.addContactLineEdit.setGeometry(QtCore.QRect(700, 80, 181, 27))
        self.addContactLineEdit.setObjectName("addContactLineEdit")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 550, 541, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.emojiButton = QtWidgets.QToolButton(self.centralwidget)
        self.emojiButton.setStyleSheet("QToolButton { border: none }")
        self.emojiButton.setIcon(QtGui.QIcon(EMOJI_PATH + "happy.png"))
        self.horizontalLayout.addWidget(self.emojiButton)

        self.messageSendTextEdit = MyTextEditWidget(self.widget)
        self.messageSendTextEdit.setObjectName("messageSendTextEdit")
        self.horizontalLayout.addWidget(self.messageSendTextEdit)
        self.sendMessagePushButton = QtWidgets.QPushButton(self.widget)
        self.sendMessagePushButton.setObjectName("sendMessagePushButton")
        self.horizontalLayout.addWidget(self.sendMessagePushButton)

        self.nonContactsWidget = QtWidgets.QWidget(self.centralwidget)
        self.nonContactsWidget.setGeometry(QtCore.QRect(710, 520, 241, 31))
        self.nonContactsWidget.setObjectName("nonContactsWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.nonContactsWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addNonContactPushButton = QtWidgets.QPushButton(self.nonContactsWidget)
        self.addNonContactPushButton.setObjectName("addNonContactPushButton")
        self.horizontalLayout_2.addWidget(self.addNonContactPushButton)
        self.ignoreNonContactPushButton = QtWidgets.QPushButton(self.nonContactsWidget)
        self.ignoreNonContactPushButton.setObjectName("ignoreNonContactPushButton")
        self.horizontalLayout_2.addWidget(self.ignoreNonContactPushButton)

        self.contactsWidget = QtWidgets.QWidget(self.centralwidget)
        self.contactsWidget.setGeometry(QtCore.QRect(710, 520, 241, 31))
        self.contactsWidget.setObjectName("contactsWidget")
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.contactsWidget)
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.deleteContactPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteContactPushButton.setGeometry(QtCore.QRect(710, 520, 241, 31))
        self.deleteContactPushButton.setObjectName("deleteContactPushButton")
        self.horizontalLayout_33.addWidget(self.deleteContactPushButton)

        self.contactsActionsBox = QtWidgets.QStackedWidget(self.centralwidget)
        self.contactsActionsBox.setGeometry(QtCore.QRect(710, 520, 241, 31))
        self.contactsActionsBox.addWidget(self.contactsWidget)
        self.contactsActionsBox.addWidget(self.nonContactsWidget)
        self.contactsActionsBox.setCurrentWidget(self.contactsWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Messenger"))
        self.ContactsCountLabel.setText(_translate("MainWindow", "Total: "))
        self.deleteContactPushButton.setText(_translate("MainWindow", "Delete"))
        self.addContactPushButton.setText(_translate("MainWindow", "Add"))
        self.userNameLabel.setText(_translate("MainWindow", "Self"))
        self.chatTextLabel.setText(_translate("MainWindow", "Chat With:"))
        self.addContactLineEdit.setPlaceholderText(_translate("MainWindow", "contact name to add"))
        self.messageSendTextEdit.setPlaceholderText(_translate("MainWindow", "type message here "))
        self.sendMessagePushButton.setText(_translate("MainWindow", "Send Message"))
        self.addNonContactPushButton.setText(_translate("MainWindow", "Add"))
        self.ignoreNonContactPushButton.setText(_translate("MainWindow", "Ignore"))
