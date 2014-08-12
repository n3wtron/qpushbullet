from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QSystemTrayIcon, QMenu, QAction, QApplication
from qpushbullet.mainwin import QPushBulletListener

__author__ = 'Igor Maculan <n3wtron@gmail.com>'


class PushbulletTray(QSystemTrayIcon):
    def __init__(self, main_win):
        QSystemTrayIcon.__init__(self)
        self.main_win = main_win
        self._init_context_menu()

    def _init_context_menu(self):
        self.setContextMenu(QMenu(None))

        settings_act = QAction('Settings', self)
        settings_act.triggered.connect(self.main_win.settings_dlg.show)
        self.contextMenu().addAction(settings_act)

        exit_act = QAction('Exit', self)
        exit_act.triggered.connect(self.main_win.exit)
        self.contextMenu().addAction(exit_act)

    @pyqtSlot(dict)
    def on_link(self, lnk):
        self.showMessage(lnk['title'], lnk['url'])

    @pyqtSlot(dict)
    def on_note(self, note):
        self.showMessage(note['title'], note['body'])

