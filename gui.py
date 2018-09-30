from PyQt5 import QtWidgets

import sys

from ui.welcome_window import WelcomeWidget


def run_client():
    app = QtWidgets.QApplication(sys.argv)
    win = WelcomeWidget()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_client()
