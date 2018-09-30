from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from ui.py_views.joinWidget import Ui_joinWidget
from ui.py_views.editPhoto import Ui_Dialog

from JIM.jim_config import *


class JoinWindow(QtWidgets.QDialog, Ui_joinWidget):
    ok_button_signal = QtCore.pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.profile_photo = None

        self.choosePhotoButton.clicked.connect(self.choose_photo)
        self.editPushButton.clicked.connect(self.edit_photo)

        self.okPushButton.clicked.connect(self.ok_bttn_clicked)
        self.cancelPushButton.clicked.connect(self.close)

    # TODO: передавать фото и email на сервер
    def ok_bttn_clicked(self):
        # Получаем логин и пароль, фото и email пока не используются
        login = self.loginLineEdit.text()
        password = self.passwordLineEdit.text()

        # генерируем сигнал для welcome_window
        if login and password:
            self.ok_button_signal.emit(REGISTER, login, password)
            self.passwordLineEdit.clear()
        else:
            self.parent().info_boxes('info', 'not enough info', 'please fill fields')

    def edit_photo(self):
        if self.profile_photo:
            editor = EditPhoto(self.profile_photo, parent=self)
            editor.save_photo_signal.connect(self.set_profile_photo)
            editor.show()

    def choose_photo(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')[0]
        if file_path:
            self.profile_photo = Image.open(file_path)
            self.set_photo(self.profile_photo)

    def set_photo(self, photo_):
        height = self.photoLabel.size().height()
        width = int(height * photo_.size[0] / photo_.size[1])

        self.profile_photo = photo_.resize((width, height), Image.ANTIALIAS)
        img_tmp = ImageQt(self.profile_photo.convert('RGBA'))
        pixmap = QtGui.QPixmap.fromImage(img_tmp)
        self.photoLabel.setPixmap(pixmap)

    def set_profile_photo(self, photo_):
        self.profile_photo = photo_
        self.set_photo(photo_)


# TODO: добавить ползунок который будет менять интенсивность изменений
class EditPhoto(QtWidgets.QDialog, Ui_Dialog):
    save_photo_signal = QtCore.pyqtSignal(object)

    def __init__(self, photo, parent=None):
        QtWidgets.QDialog.__init__(self, parent=parent)
        self.photo = photo
        self.tmp_photo = None

        self.photo_width = self.photo.size[0]
        self.photo_height = self.photo.size[1]

        self.setupUi(self)
        self.set_photo(self.photo)

        self.grayPushButton.clicked.connect(self.grey)
        self.blackAndWhitePushButton.clicked.connect(self.black_and_white)
        self.negaitvePushButton.clicked.connect(self.negative)
        self.sepiaPushButton.clicked.connect(self.sepia)
        self.savePushButton.clicked.connect(self.save_photo)
        self.cancelPushButton.clicked.connect(self.close)

    def set_photo(self, photo_):
        img_tmp = ImageQt(photo_.convert('RGBA'))
        pixmap = QtGui.QPixmap.fromImage(img_tmp)
        self.editorLabel.setPixmap(pixmap)

    def grey(self):
        self.tmp_photo = self.photo.copy()
        pix = self.tmp_photo.load()
        draw = ImageDraw.Draw(self.tmp_photo)
        for i in range(self.photo_width):
            for j in range(self.photo_height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                draw.point((i, j), (S, S, S))
        self.set_photo(self.tmp_photo)

    def black_and_white(self):
        self.tmp_photo = self.photo.copy()
        pix = self.tmp_photo.load()
        draw = ImageDraw.Draw(self.tmp_photo)
        factor = 30
        for i in range(self.photo_width):
            for j in range(self.photo_height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                s = a + b + c
                if s > (((255 + factor) // 2) * 3):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                draw.point((i, j), (a, b, c))
        self.set_photo(self.tmp_photo)

    def negative(self):
        self.tmp_photo = self.photo.copy()
        pix = self.tmp_photo.load()
        draw = ImageDraw.Draw(self.tmp_photo)
        for i in range(self.photo_width):
            for j in range(self.photo_height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                draw.point((i, j), (255 - a, 255 - b, 255 - c))
        self.set_photo(self.tmp_photo)

    def sepia(self):
        self.tmp_photo = self.photo.copy()
        pix = self.tmp_photo.load()
        draw = ImageDraw.Draw(self.tmp_photo)
        depth = 60
        for i in range(self.photo_width):
            for j in range(self.photo_height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                a = S + depth * 2
                b = S + depth
                c = S
                if a > 255:
                    a = 255
                if b > 255:
                    b = 255
                if c > 255:
                    c = 255
                draw.point((i, j), (a, b, c))
        self.set_photo(self.tmp_photo)

    def save_photo(self):
        self.save_photo_signal.emit(self.tmp_photo)
        self.close()
