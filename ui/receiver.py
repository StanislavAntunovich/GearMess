from PyQt5 import QtCore

from JIM.jim_config import *


class Receiver(QtCore.QThread):
    new_message_signal = QtCore.pyqtSignal(dict)

    def __init__(self, service_queue, user, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.service_queue = service_queue
        self.on_line = False
        self.user = user

    def run(self):
        self.on_line = True
        while self.on_line:
            message = self.parent().user.receive()
            if message:
                if message.get(MESSAGE):
                    self.new_message_signal.emit(message)
                else:
                    self.service_queue.put(message)
