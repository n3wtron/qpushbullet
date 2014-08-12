__author__ = 'Igor Maculan <n3wtron@gmail.com>'
import sys

from PyQt4.QtGui import QApplication

from qpushbullet.mainwin import MainWindow
from qpushbullet.tray import PushbulletTray

import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    app = QApplication(sys.argv)
    #app.setQuitOnLastWindowClosed(False)
    main_win = MainWindow()

    tray = PushbulletTray(main_win)
    main_win.connect_systray(tray)
    tray.show()

    main_win.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()