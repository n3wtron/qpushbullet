from qpushbullet.mainwin import MainWindow
from qpushbullet.tray import PushbulletTray

__author__ = 'Igor Maculan <n3wtron@gmail.com>'
import sys

from PyQt4.QtGui import QApplication

import logging

logging.basicConfig(level=logging.DEBUG)


def main():
    app = QApplication(sys.argv)
    MainWindow(app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()