from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QSystemTrayIcon, QMenu, QAction, QIcon

__author__ = 'Igor Maculan <n3wtron@gmail.com>'


class PushbulletTray(QSystemTrayIcon):
    def __init__(self, main_win):
        QSystemTrayIcon.__init__(self,main_win)
        self.setIcon(QIcon(':/icons/logo16_disabled'))
        self.main_win = main_win
        self._init_context_menu()
        self.activated.connect(self.show_main_window)

    @pyqtSlot(QSystemTrayIcon.ActivationReason)
    def show_main_window(self, reason):
        if reason == self.DoubleClick and self.main_win:
            if self.main_win.isVisible():
                self.main_win.hide()
            else:
                self.main_win.show()

    @pyqtSlot(bool)
    def connected(self, connected):
        if connected:
            self.setIcon(QIcon(':/icons/logo16'))
        else:
            self.setIcon(QIcon(':/icons/logo16_disabled'))

    def _init_context_menu(self):
        self.setContextMenu(QMenu(None))

        settings_act = QAction('Settings', self)
        settings_act.setIcon(QIcon.fromTheme("preferences-system"))
        settings_act.triggered.connect(self.main_win.settings_dlg.show)
        self.contextMenu().addAction(settings_act)

        exit_act = QAction('Exit', self)
        exit_act.setIcon(QIcon.fromTheme("application-exit"))
        exit_act.triggered.connect(self.main_win.exit)
        self.contextMenu().addAction(exit_act)

    @pyqtSlot(dict)
    def on_link(self, lnk):
        self.showMessage(lnk['title'], lnk['url'])

    @pyqtSlot(dict)
    def on_note(self, note):
        self.showMessage(note['title'], note['body'])

