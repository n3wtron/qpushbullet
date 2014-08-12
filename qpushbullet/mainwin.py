import os

__author__ = 'Igor Maculan <n3wtron@gmail.com>'
from PyQt4.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt4.QtGui import QMainWindow, QApplication, QListWidgetItem, QFileDialog

from pushbullet import Listener, PushBullet
from qpushbullet import config
from qpushbullet.settings import SettingsDlg
from ui.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.listener = None
        self.tray = None
        self.pusher = None
        self.connect_pushbullet()
        self.settings_dlg = SettingsDlg(self)
        self.settings_dlg.saved.connect(self.reconnect)
        self.ui.action_Settings.triggered.connect(self.settings_dlg.show)
        self.ui.browseFileBtn.clicked.connect(self.choice_file)

    @pyqtSlot()
    def choice_file(self):
        file_to_send = QFileDialog.getOpenFileName(self, "chosse file to send")
        if file_to_send and not file_to_send.isEmpty():
            self.ui.filePathEdt.setText(file_to_send)

    def refresh_devices(self):
        self.ui.devicesList.clear()
        for device in self.pusher.devices:
            device_item = QListWidgetItem(device.name)
            device_item.setData(Qt.UserRole, device)
            self.ui.devicesList.addItem(device_item)

    def connect_pushbullet(self):
        if config.value('key') is not None and not config.value('key').toString().isEmpty():
            proxy_host = str(config.value('proxy.host').toString())
            proxy_port, int_conv_ok = config.value('proxy.port').toInt()
            if proxy_host.strip() == '':
                proxy_host = proxy_port = None
            self.listener = QPushBulletListener(self, str(config.value('key').toString()), proxy_host, proxy_port)
            self.listener.start()
            self.pusher = PushBullet(str(config.value('key').toString()))
            self.refresh_devices()
            self.connect_pushes()

    def disconnect_pushbullet(self):
        if self.listener is not None:
            self.listener.quit()
            if self.listener.isRunning():
                self.listener.terminate()
            self.disconnect_systray()
            self.listener = None
            self.disconnect_pushes()

    @pyqtSlot()
    def push_note(self):
        if self.pusher and self.ui.devicesList.currentItem():
            device = self.ui.devicesList.currentItem().data(Qt.UserRole).toPyObject()
            device.push_note(str(self.ui.noteTitleEdt.text()), str(self.ui.noteTextEdt.toPlainText()))

    @pyqtSlot()
    def push_link(self):
        if self.pusher and self.ui.devicesList.currentItem():
            device = self.ui.devicesList.currentItem().data(Qt.UserRole).toPyObject()
            device.push_link(str(self.ui.linkTitleEdt.text()), str(self.ui.linkUrlEdt.text()))

    @pyqtSlot()
    def push_file(self):
        if self.pusher and self.ui.devicesList.currentItem():
            device = self.ui.devicesList.currentItem().data(Qt.UserRole).toPyObject()
            fname = str(self.ui.filePathEdt.text())
            device.push_file(open(fname))

    def connect_pushes(self):
        self.ui.sendNoteBtn.clicked.connect(self.push_note)
        self.ui.sendLinkBtn.clicked.connect(self.push_link)
        self.ui.sendFileBtn.clicked.connect(self.push_file)

    def disconnect_pushes(self):
        self.ui.sendNoteBtn.clicked.disconnect(self.push_note)
        self.ui.sendLinkBtn.clicked.disconnect(self.push_link)
        self.ui.sendFileBtn.clicked.disconnect(self.push_file)

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
            self.disconnect_pushbullet()
        self.connect_pushbullet()

    @pyqtSlot()
    def exit(self):
        self.disconnect_pushbullet()
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
