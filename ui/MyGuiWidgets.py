from PyQt5 import QtGui, QtCore, QtWidgets
from os.path import abspath, join

STRING_HIGH = 24
CONTACT_BACKGROUND_COLOR = 'light green'
NON_CONTACT_BACKGROUND_COLOR = 'yellow'
NO_COLOR = 'white'


class MyListWidget(QtWidgets.QListWidget):
    del_contact_signal = QtCore.pyqtSignal(str)
    add_contact_signal = QtCore.pyqtSignal(str)
    remove_and_ignore_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            if event.y() < self.count() * STRING_HIGH:
                self.setCurrentRow(event.y() // STRING_HIGH)
                if self.currentItem().in_contacts:
                    self.context_menu_for_contacts(event)
                else:
                    self.context_menu_for_non_contacts(event)
        super().mousePressEvent(event)

    def context_menu_for_contacts(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addAction('delete', self.context_del_contact)
        menu.exec(event.globalPos())

    def context_menu_for_non_contacts(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addAction('add contact', self.context_add_contact)
        menu.addSeparator()
        menu.addAction('remove and ignore', self.context_remove_and_ignore)
        menu.exec(event.globalPos())

    def context_add_contact(self):
        name = self.currentItem().text()
        self.add_contact_signal.emit(name)

    def contact_added(self, contact_item):
        contact = self.currentItem() if not contact_item else contact_item
        if contact.background() == QtGui.QColor(NON_CONTACT_BACKGROUND_COLOR):
            contact.setBackground(QtGui.QColor(CONTACT_BACKGROUND_COLOR))

    def context_del_contact(self):
        name = self.currentItem().text()
        self.del_contact_signal.emit(name)

    def context_remove_and_ignore(self):
        name = self.currentItem().text()
        self.takeItem(self.currentRow())
        self.remove_and_ignore_signal.emit(name)

    def new_message_icon(self, item_):
        item_.messages_count += 1
        if item_.messages_count <= 10:
            icon_file = '{}.png'.format(item_.messages_count)
            icon = join(abspath('.'), 'ui', 'numbers_icons', icon_file)
        else:
            icon = join(abspath('.'), 'ui', 'numbers_icons', '11')
        item_.setIcon(QtGui.QIcon(icon))

    def new_message(self, name):
        item = self.findItems(name, QtCore.Qt.MatchExactly)
        if not item:
            new_contact = self.addItem(name)
            new_contact.setBackground(QtGui.QColor(NON_CONTACT_BACKGROUND_COLOR))
            self.new_message_icon(new_contact)
        else:
            contact = item[0]
            if contact.in_contacts:
                contact.setBackground(QtGui.QColor(CONTACT_BACKGROUND_COLOR))
            else:
                contact.setBackground(QtGui.QColor(NON_CONTACT_BACKGROUND_COLOR))
            self.new_message_icon(contact)

    def item_double_clicked(self):
        self.currentItem().messages_count = 0
        self.currentItem().setBackground(QtGui.QColor(NO_COLOR))
        self.currentItem().setIcon(QtGui.QIcon(''))

    def add_contact(self, contact_name):
        contact = self.findItems(contact_name, QtCore.Qt.MatchExactly)
        if contact:
            new_contact = contact[0]
            self.contact_added(new_contact)
        else:
            new_contact = self.addItem(contact_name)
        new_contact.in_contacts = True

    def add_contacts(self, contacts_list):
        for contact in contacts_list:
            self.add_contact(contact)

    def addItem(self, *__args):
        item = MyListItem(*__args)
        super().addItem(item)
        return item


class MyListItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages_count = 0
        self.in_contacts = False
        self.setSizeHint(QtCore.QSize(-1, STRING_HIGH))


class MyTextEditWidget(QtWidgets.QTextEdit):
    send_message_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.send_message_shortcut_id = self.grabShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return))

    def event(self, event_):
        if event_.type() == QtCore.QEvent.Shortcut:
            if event_.shortcutId() == self.send_message_shortcut_id:
                self.send_message_signal.emit()
        return super().event(event_)
