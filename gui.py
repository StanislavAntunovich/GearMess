from PyQt5 import QtWidgets
import sys

from ui.welcome_window import WelcomeWidget


# TODO: добавить config и считывать настройки configparser'ом
# TODO: добавить функцию задания настроек соединения которые будут считываться из config
HOST = '151.248.121.11'
PORT = 6666
BUFFER = 4048


def run_client():
    app = QtWidgets.QApplication(sys.argv)
    win = WelcomeWidget(host=HOST, port=PORT, buff_size=BUFFER)
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_client()
