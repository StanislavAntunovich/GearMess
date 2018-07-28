# настроить базу истории сообщений... на стороне сервера тоже...

"""
Сделано:
    - при двойном клике - выгрузка истории сообщений с контактом и отправка адресных сообщений
    - если приходит сообщение не от того с кем общаемся - его контакт в листе подсвечивается зеленым
    - если приходит сообщение от незнакомца - подсвечивается желтым в списке контактов но не добаляется (если добавить
        будет два одинаковых до след загрузки

планы:
    - при выгрузке сообщений по двойному клику курсор в конец, чтобы не листать вниз
    - избавиться об чрезмерной связанности - реализовать класс связывающий между собой окошки, базу и логику клиента:
      * окошки посылают (и принимают?) только сигналы
      * класс обрабатывает сигналы и отправляет результаты в окошки/базу
    - разобраться с - модели/представления контакт листа - возможно через базу
    ? возможно открывать чат в новом окошке
    - добавить меню - натсройки отображения истории сообщений за выбранный период и адрес/порт сервера
    - потом при запуске выгрузка с сервера пропущенных сообщений
    - при нажатии Enter отправлять сообщение *или добавлять контакт *или начинать чат
    и устанавливать фокус ввода в нужном месте
    - при сообщении от неизвестного - возможность добавить в контакт лист правой кнопкой(позже- возможность заблокировать)

"""

from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import queue
import threading
from time import sleep

from GearMess.client_src._client import Client
from GearMess.JIM.jim_config import *

from GearMess.client_src.client_views import Ui_Dialog, Ui_MainWindow



class LoginPage(QtWidgets.QDialog, Ui_Dialog):
    """ Стартовое окно при запуске приложения, для воода данных,
     передает сигнал с личными данными и адресом сокета в основное окно,
      если данные сокета не введены - использует значения по умолчанию"""

    welcomeSignal = QtCore.pyqtSignal(str, str, str, str, int)

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)

        self.setupUi(self)

        self.warningWindow = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 'oops', '',
                                                   buttons=QtWidgets.QMessageBox.Ok, parent=self)
        self.loginPushButton.clicked.connect(lambda: self.welcomeWindowSignal('login'))
        self.joinPushButton.clicked.connect(lambda: self.welcomeWindowSignal('join'))

    # доработать - чтобы при отсутствии одного из значений подставлялось по умолчанию,
    #  а не двух сразу и выбрасывать оконо ошибки если формат данных не соответствует
    def welcomeWindowSignal(self, action):

        user_name = self.loginTextEdit.text()
        password = self.passwordTextEdit.text()
        host = self.hostTextEdit.text()
        port = self.portTextEdit.text()
        if user_name and host and port:
            self.welcomeSignal.emit(action, user_name, password, host, int(port))
        else:
            self.welcomeSignal.emit(action, user_name, password, 'localhost', 7777)

    # магический метод
    def on_cancelPushButton_clicked(self):
        # заменить ... не понял как выйти из всего приложения
        sys.exit(-1)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    errorSignal = QtCore.pyqtSignal(str, str)
    questionSignal = QtCore.pyqtSignal(str, str)
    incomeMessageSignal = QtCore.pyqtSignal(dict)  # попробуем как временное решение

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.welcomeWindow = LoginPage(parent=self)
        self.questionWindow = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, 'are you sure?', '???',
                                                    buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    parent=self)
        self.warningWindow = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 'oops', '!!!',
                                                   buttons=QtWidgets.QMessageBox.Ok, parent=self)

        self.serviceQueue = queue.Queue()
        self.receiver = threading.Thread(target=self.receive)
        self.resp_event = threading.Event()

        self.addContactPushBotton.clicked.connect(self.add_contact)
        self.deleteContactPushBotton.clicked.connect(self.del_contact)
        self.sendMessagePushButton.clicked.connect(self.send_message)

        self.contactsListWidget.itemDoubleClicked.connect(self.contact_list_double_click)

        self.welcomeWindow.welcomeSignal.connect(self.welcome)
        self.errorSignal.connect(self._errorSignal)
        self.questionSignal.connect(self._questionSignal)
        self.incomeMessageSignal.connect(self.log_income_message)

        self._online = False  # сделать так вместо внутри потока приема
        self._chat_with = '#all'
        self.user = None

        self.on_start()

    def log_income_message(self, message):
        self.user.storage_handler.log_incoming_message(message)

    def welcome(self, action, name, password, host, port):
        """ Принимает сигнал\данные из loginPage и посылает соответвующий запрос на сервер,
         если код ответа положительный - закрывает loginPage, если нет - выводит ошибку в диалоговом окне"""
        self.user = Client(name, host, port)
        user_password = password

        if action == 'join':
            resp = self.user.send_registration(user_password)
            res = self.welcome_response(resp)
            return res
        elif action == 'login':
            resp = self.user.send_authorisation(user_password)
            res = self.welcome_response(resp)
            return res

    # возможно сделать с передачей любого респонса в любом месте
    def welcome_response(self, resp):
        if resp[RESPONSE] == OK:
            self.welcomeWindow.close()
            return True
        else:
            self.errorSignal.emit('oops', resp[ERROR])
            return False

    def _errorSignal(self, title, text):
        """ Задает заголовок и текст сообщения об ошибке, открывает диалоговое окно"""
        self.warningWindow.setWindowTitle(title)
        self.warningWindow.setText(text)
        self.warningWindow.exec()

    # доработать - избавиться от dialog_to_del_contact()
    def _questionSignal(self, title, text):
        self.questionWindow.setWindowTitle(title)
        self.questionWindow.setText(text)
        # choice = self.questionWindow.exec()
        # return choice

    def set_contacts_label(self):
        contacts_count = self.contactsListWidget.count() - 1
        self.ContactsContLabel.setText(f'Total: {contacts_count}')

    def set_chat_name(self, name):
        self.chatTextLabel.setText(name)

    def send_message(self):
        """ Берет текст сообщения из поля для ввода и отправляет на сервер, в качестве адресата берет chat_with """
        message = self.messageTextEdit.toPlainText()
        message_to_ins = '<b><span style=\" color: grey;\">я: {}</span></b><br>'.format(message)
        self.ChatBrowser.insertHtml(message_to_ins)
        self.messageTextEdit.clear()
        self.user.send_message(message=message, to=self._chat_with)

    # доработать - чтоб сам выбирал стилизацию - я пишу или мне пишут
    def printMessage(self, message):
        """ Выводит сообщения на экран """
        self.ChatBrowser.insertPlainText(message + '\n')

    def add_contact(self):
        contact = self.addContactTextEdit.toPlainText()
        if contact:
            self.addContactTextEdit.clear()
            self.user.add_contact(contact)
            # self.resp_event.wait()
            resp = self.serviceQueue.get()
            if resp[RESPONSE] == OK:
                self.contactsListWidget.addItem(contact)
                self.set_contacts_label()
            else:
                self.errorSignal.emit('oops', resp[ERROR])
        else:
            self.errorSignal.emit('add contact', 'поле должно быть заполнено')

    # пдоумать как разбить
    def del_contact(self):
        contact_in_list = self.contactsListWidget.currentRow()
        if contact_in_list:
            contact_name = self.contactsListWidget.currentItem().text()
            if self.dialog_to_del_contact(contact_name):
                self.user.del_contact(contact_name)
                # self.resp_event.wait()
                resp_ = self.serviceQueue.get()
                if resp_[RESPONSE] == OK:
                    self.contactsListWidget.takeItem(contact_in_list)
                    self.set_contacts_label()
                else:
                    self.errorSignal.emit('oops', resp_[ERROR])
        else:
            self.errorSignal.emit('Delete contact', 'поле должно быть заполнено')

    # c этим еще поразбираться - нельзя удалить первую строку - покачто там ссылка на общий чат
    def get_contacts(self):
        _all = ['#all']
        self.user.get_contacts()
        # self.resp_event.wait()
        contacts = self.serviceQueue.get()['contact_list']
        self.contactsListWidget.addItems(_all + contacts)
        self.set_contacts_label()

    # понять как перелистывать сразу вниз страницы
    def contact_list_double_click(self):
        """ Выгружает сообщения с выбранным пользователем из базы и меняет адресата исходящих сообщений на выбранный"""
        self.contactsListWidget.currentItem().setBackground(QtGui.QColor('white'))
        name = self.contactsListWidget.currentItem().text()
        self._chat_with = name
        format_name = 'Chat with: {}'.format(name)
        self.chatTextLabel.setText(format_name)
        self.ChatBrowser.clear()
        if name != '#all':
            history_ = self.user.storage_handler.messages_history(name)
            for message in history_:
                if message[FROM] == self.user.name:
                    message_to_ins = '<b><span style=\" color: grey;\">{}- я: {}</span></b><br>'. \
                        format(message[TIME], message[MESSAGE])
                else:
                    message_to_ins = '<span style=\" color: black;\">{}- {}: {}</span><br>'. \
                        format(message[TIME], message[FROM], message[MESSAGE])
                self.ChatBrowser.insertHtml(message_to_ins)

    def dialog_to_del_contact(self, name):
        textPattern = 'Are you sure to delete "{}"?'.format(name)
        self.questionSignal.emit('Delete contact', textPattern)
        choice = self.questionWindow.exec()
        if choice == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def returnPressed(self):
        """ будет использоваться как обработчик нажатия клавиши Enter для оптравки сообщений или добавления контакта"""
        pass

    def receive(self):
        """ Цикл приема сообщений для использования в потоке.
            Если приходит сообщение не от того с кем мы в данный момент общаемся - подсвечивает его в списке зеленым"""
        self._online = True
        while self._online:
            try:
                message = self.user.receive()
            except:
                pass
            else:
                # разгрести это нагромождение!!!
                if message.get(MESSAGE):
                    self.incomeMessageSignal.emit(message)
                    if message[FROM] != self.user.name and message[FROM] == self._chat_with:
                        self.ChatBrowser.insertPlainText('{}: {}'.format(message[FROM], message[MESSAGE]) + '\n')
                    else:
                        cont = self.contactsListWidget.findItems(message[FROM], QtCore.Qt.MatchExactly)
                        if cont:
                            cont[0].setBackground(QtGui.QColor('light green'))
                        else:
                            if message[FROM] != self.user.name:
                                self.contactsListWidget.addItem(message[FROM])
                                cont = self.contactsListWidget.findItems(message[FROM], QtCore.Qt.MatchExactly)
                                cont[0].setBackground(QtGui.QColor('yellow'))
                else:
                    self.serviceQueue.put(message)
                    # self.resp_event.set()

    def on_start(self):
        # TODO: сделать так чтобы без авторизации не пускало в основное окно (решится при реализации отдельного класса)
        self.welcomeWindow.exec()
        # self._online = True
        self.receiver.start()
        self.get_contacts()
        self.user.send_presence()
        self.userNameLabel.setText(self.user.name)

    # Переопределяем метод, вызываемый при закртии основного окна -
    # посылает quit- сообщение на сервер и дает возможность доработать потоку
    def closeEvent(self, event):
        self.hide()
        self._online = False
        self.user.quit_server()
        sleep(2)  # возможно есть метод как у Qt ожидающий завершения работы потока
        event.accept()


def start_client():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_client()
