# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\welcomeWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_welcomeFirstWidget(object):
    def setupUi(self, welcomeFirstWidget):
        welcomeFirstWidget.setObjectName("welcomeFirstWidget")
        welcomeFirstWidget.resize(277, 355)

        self.gridLayout_2 = QtWidgets.QGridLayout(welcomeFirstWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(welcomeFirstWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.loginPushButton = QtWidgets.QPushButton(self.splitter)
        self.loginPushButton.setAutoDefault(False)
        self.loginPushButton.setDefault(True)
        self.loginPushButton.setObjectName("loginPushButton")
        self.joinPushButton = QtWidgets.QPushButton(self.splitter)
        self.joinPushButton.setAutoDefault(False)
        self.joinPushButton.setObjectName("joinPushButton")
        self.verticalLayout.addWidget(self.splitter)
        self.cancelPushButton = QtWidgets.QPushButton(welcomeFirstWidget)
        self.cancelPushButton.setAutoDefault(False)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.verticalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(31, 158, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(31, 158, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(welcomeFirstWidget)
        QtCore.QMetaObject.connectSlotsByName(welcomeFirstWidget)

    def retranslateUi(self, welcomeFirstWidget):
        _translate = QtCore.QCoreApplication.translate
        welcomeFirstWidget.setWindowTitle(_translate("welcomeFirstWidget", "Welcome"))
        self.loginPushButton.setText(_translate("welcomeFirstWidget", "Login"))
        self.joinPushButton.setText(_translate("welcomeFirstWidget", "Join"))
        self.cancelPushButton.setText(_translate("welcomeFirstWidget", "Cancel"))
