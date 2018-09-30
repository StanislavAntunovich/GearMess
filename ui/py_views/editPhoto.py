# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\editPhoto.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from PIL.ImageQt import ImageQt
from PIL import Image, ImageDraw


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(626, 486)
        self.editorLabel = QtWidgets.QLabel(Dialog)
        self.editorLabel.setGeometry(QtCore.QRect(12, 49, 591, 371))
        self.editorLabel.setText("")
        self.editorLabel.setObjectName("editorLabel")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(11, 445, 601, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(399, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.savePushButton = QtWidgets.QPushButton(self.widget)
        self.savePushButton.setObjectName("savePushButton")
        self.horizontalLayout.addWidget(self.savePushButton)
        self.cancelPushButton = QtWidgets.QPushButton(self.widget)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(12, 12, 601, 30))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sepiaPushButton = QtWidgets.QPushButton(self.widget1)
        self.sepiaPushButton.setObjectName("sepiaPushButton")
        self.horizontalLayout_2.addWidget(self.sepiaPushButton)
        self.grayPushButton = QtWidgets.QPushButton(self.widget1)
        self.grayPushButton.setObjectName("grayPushButton")
        self.horizontalLayout_2.addWidget(self.grayPushButton)
        self.negaitvePushButton = QtWidgets.QPushButton(self.widget1)
        self.negaitvePushButton.setObjectName("negaitvePushButton")
        self.horizontalLayout_2.addWidget(self.negaitvePushButton)
        self.blackAndWhitePushButton = QtWidgets.QPushButton(self.widget1)
        self.blackAndWhitePushButton.setObjectName("blackAndWhitePushButton")
        self.horizontalLayout_2.addWidget(self.blackAndWhitePushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.savePushButton.setText(_translate("Dialog", "Save"))
        self.cancelPushButton.setText(_translate("Dialog", "Cancel"))
        self.sepiaPushButton.setText(_translate("Dialog", "Sepia"))
        self.grayPushButton.setText(_translate("Dialog", "Gray"))
        self.negaitvePushButton.setText(_translate("Dialog", "Negative"))
        self.blackAndWhitePushButton.setText(_translate("Dialog", "Black and White"))
