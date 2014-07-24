__author__ = 'Igor Maculan <n3wtron@gmail.com>'
from PyQt4.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QMainWindow, QApplication
from pushbullet import Listener

from qpushbullet import config
from qpushbullet.settings import SettingsDlg


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.listener = None
        self.tray = None
        self.connect_listener()
        self.settings_dlg = SettingsDlg(self)
        self.settings_dlg.saved.connect(self.reconnect)

    def connect_listener(self):
        if config.value('key') is not None and not config.value('key').toString().isEmpty():
            proxy_host = str(config.value('proxy.host').toString())
            proxy_port, int_conv_ok = config.value('proxy.port').toInt()
            if proxy_host.strip() == '' or proxy_port.strip() == '':
                proxy_host = proxy_port = None
            self.listener = QPushBulletListener(self, str(config.value('key').toString()), proxy_host, proxy_port)
            self.listener.start()

    def disconnect_listener(self):
        if self.listener is not None:
            self.listener.quit()
            if self.listener.isRunning():
                self.listener.terminate()
            self.disconnect_systray()
            self.listener = None

    def connect_systray(self, tray):
        self.tray = tray
        if self.tray is not None:
            self.listener.on_link.connect(self.tray.on_link)
            self.listener.on_note.connect(self.tray.on_note)

    def disconnect_systray(self):
        if self.tray is not None:
            self.listener.on_link.disconnect(self.tray.on_link)
            self.listener.on_note.disconnect(self.tray.on_note)

    @pyqtSlot()
    def reconnect(self):
        if self.listener is not None:
            self.disconnect_listener()
        self.connect_listener()

    @pyqtSlot()
    def exit(self):
        self.disconnect_listener()
        QApplication.quit()

    def closeEvent(self, event):
        self.listener.quit()
        QMainWindow.closeEvent(self, event)


class QPushBulletListener(QThread):
    # signals
    on_link = pyqtSignal(dict)
    on_note = pyqtSignal(dict)
    on_list = pyqtSignal(dict)
    on_file = pyqtSignal(dict)
    on_address = pyqtSignal(dict)

    def __init__(self, parent, api_key, http_proxy_host=None, http_proxy_port=None):
        QThread.__init__(self, parent)
        self.listener = Listener(api_key,
                                 on_link=self.on_link_handle,
                                 on_address=self.on_address_handle,
                                 on_file=self.on_file_handle,
                                 on_note=self.on_note_handle,
                                 on_list=self.on_list_handle,
                                 http_proxy_host=http_proxy_host,
                                 http_proxy_port=http_proxy_port)

    def on_link_handle(self, lnk):
        self.on_link.emit(lnk)

    def on_address_handle(self, addr):
        self.on_address.emit(addr)

    def on_note_handle(self, note):
        self.on_note.emit(note)

    def on_list_handle(self, lst):
        self.on_list.emit(lst)

    def on_file_handle(self, fl):
        self.on_file.emit(fl)

    def run(self):
        self.listener.run_forever()

    def quit(self):
        self.listener.close()
        timeout = 0
        # wait 10sec to close the websocket
        while self.listener.connected and timeout < 30:
            self.sleep(1)
            timeout += 1

        QThread.quit(self)
