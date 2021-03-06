import os
import time

from qpushbullet.tray import PushbulletTray


__author__ = 'Igor Maculan <n3wtron@gmail.com>'
from PyQt4.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt4.QtGui import QMainWindow, QListWidgetItem, QFileDialog, QIcon, QMessageBox
from pushbullet import Listener, PushBullet
from qpushbullet import config
from qpushbullet.settings import SettingsDlg
from ui.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    connected = pyqtSignal(bool)

    def __init__(self, app):
        QMainWindow.__init__(self)
        self.app = app
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._exit = False
        self.ui.action_Exit.triggered.connect(self.exit)
        self.ui.actionAbout_Qt.triggered.connect(app.aboutQt)
        self.setWindowIcon(QIcon(':/icons/logo32'))
        self.listener = None
        self.tray = None
        self.pusher = None
        self._connected = False

        self.settings_dlg = SettingsDlg(self)
        self.settings_dlg.saved.connect(self.reconnect)

        self.tray = PushbulletTray(self)
        self.connect_actions()
        self.connect_pushbullet()

        self.tray.show()

    def connect_actions(self):
        self.ui.action_Settings.triggered.connect(self.settings_dlg.show)
        self.ui.browseFileBtn.clicked.connect(self.choice_file)
        self.ui.action_Refresh.triggered.connect(self.refresh)
        # List Items
        self.ui.addItemBtn.clicked.connect(self.add_item_list)
        self.ui.removeItemBtn.clicked.connect(self.remove_item_list)
        self.ui.clearItemsBtn.clicked.connect(self.clear_item_list)
        self.ui.itemsList.itemDoubleClicked.connect(self.edit_item_list)

    @pyqtSlot()
    def add_item_list(self):
        item = QListWidgetItem("item", self.ui.itemsList)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.ui.itemsList.addItem(item)

    @pyqtSlot()
    def remove_item_list(self):
        if self.ui.itemsList.currentRow() >= 0:
            self.ui.itemsList.takeItem(self.ui.itemsList.currentRow())

    @pyqtSlot()
    def clear_item_list(self):
        self.ui.itemsList.clear()

    @pyqtSlot(QListWidgetItem)
    def edit_item_list(self, item):
        self.ui.itemsList.editItem(item)

    @pyqtSlot()
    def choice_file(self):
        file_to_send = QFileDialog.getOpenFileName(self, "choose file to send")
        if file_to_send and not file_to_send.isEmpty():
            self.ui.filePathEdt.setText(file_to_send)

    @pyqtSlot()
    def refresh(self):
        self.refresh_devices()

    @pyqtSlot()
    def refresh_devices(self):
        self.ui.devicesList.clear()
        for device in self.pusher.devices:
            device_item = QListWidgetItem(device.nickname)
            device_item.setData(Qt.UserRole, device)
            self.ui.devicesList.addItem(device_item)

    def connect_pushbullet(self):
        if config.value('key') is not None and not config.value('key').toString().isEmpty():
            proxy_host = str(config.value('proxy.host').toString())
            proxy_port, int_conv_ok = config.value('proxy.port').toInt()
            if proxy_host.strip() == '':
                proxy_host = proxy_port = None
            self.pusher = PushBullet(str(config.value('key').toString()))
            self.listener = QPushBulletListener(self, self.pusher, proxy_host, proxy_port)
            self.listener.start()
            self.connect_systray()
            self.connect_pushes_actions()
            self.refresh_devices()
            self.connected.emit(True)
            self._connected = True
        else:
            self.connected.emit(False)

    def disconnect_pushbullet(self):
        self.connected.emit(False)
        if False and self.listener is not None:
            print "systray"
            self.disconnect_systray()
            print "listener quit"
            self.listener.quit()
            print "listener terminate"
            self.listener.terminate()
            print "disconnect_pushes"
            self.disconnect_pushes_actions()
            self.listener = None


    @pyqtSlot()
    def push_note(self):
        if self.pusher and len(self.ui.devicesList.selectedItems()) == 1:
            device = self.ui.devicesList.selectedItems()[0].data(Qt.UserRole).toPyObject()
            device.push_note(str(self.ui.noteTitleEdt.text()), str(self.ui.noteTextEdt.toPlainText()))
        else:
            QMessageBox.warning(self, "Cannot push", "There is no target device selected")

    @pyqtSlot()
    def push_link(self):
        if self.pusher and len(self.ui.devicesList.selectedItems()) == 1:
            device = self.ui.devicesList.selectedItems()[0].data(Qt.UserRole).toPyObject()
            device.push_link(str(self.ui.linkTitleEdt.text()), str(self.ui.linkUrlEdt.text()))
        else:
            QMessageBox.warning(self, "Cannot push", "There is no target device selected")

    @pyqtSlot()
    def push_list(self):
        if self.pusher and len(self.ui.devicesList.selectedItems()) == 1:
            device = self.ui.devicesList.selectedItems()[0].data(Qt.UserRole).toPyObject()
            widget_items = [self.ui.itemsList.item(n) for n in range(0, self.ui.itemsList.count())]
            items = map(lambda x: str(x.text()), widget_items)
            device.push_list(str(self.ui.listTitleEdt.text()), items)
        else:
            QMessageBox.warning(self, "Cannot push", "There is no target device selected")

    @pyqtSlot()
    def push_file(self):
        if self.pusher and len(self.ui.devicesList.selectedItems()) == 1:
            device = self.ui.devicesList.selectedItems()[0].data(Qt.UserRole).toPyObject()
            fname = str(self.ui.filePathEdt.text())
            with open(fname, "rb") as f_to_send:
                success, file_data = self.pusher.upload_file(f_to_send, os.path.basename(fname))
                if success:
                    device.push_file(**file_data)
        else:
            QMessageBox.warning(self, "Cannot push", "There is no target device selected")

    @pyqtSlot()
    def push_address(self):
        if self.pusher and len(self.ui.devicesList.selectedItems()) == 1:
            device = self.ui.devicesList.selectedItems()[0].data(Qt.UserRole).toPyObject()
            device.push_address(str(self.ui.addressTitleEdt.text()), str(self.ui.addressTxt.toPlainText()))
        else:
            QMessageBox.warning(self, "Cannot push", "There is no target device selected")

    def connect_pushes_actions(self):
        self.ui.sendNoteBtn.clicked.connect(self.push_note)
        self.ui.sendLinkBtn.clicked.connect(self.push_link)
        self.ui.sendFileBtn.clicked.connect(self.push_file)
        self.ui.sendListBtn.clicked.connect(self.push_list)
        self.ui.sendAddressBtn.clicked.connect(self.push_address)

    def disconnect_pushes_actions(self):
        self.ui.sendNoteBtn.clicked.disconnect(self.push_note)
        self.ui.sendLinkBtn.clicked.disconnect(self.push_link)
        self.ui.sendFileBtn.clicked.disconnect(self.push_file)
        self.ui.sendListBtn.clicked.disconnect(self.push_list)
        self.ui.sendAddressBtn.clicked.disconnect(self.push_address)

    def connect_systray(self, ):
        if self.tray is not None:
            self.connected.connect(self.tray.connected)
            self.listener.on_link.connect(self.tray.on_link)
            self.listener.on_note.connect(self.tray.on_note)
            self.connected.emit(self._connected)

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
        self._exit = True
        self.close()

    def closeEvent(self, event):
        if not self._exit:
            self.hide()
            event.ignore()
        else:
            QMainWindow.closeEvent(self, event)


class QPushBulletListener(QThread):
    # signals
    on_link = pyqtSignal(dict)
    on_note = pyqtSignal(dict)
    on_list = pyqtSignal(dict)
    on_file = pyqtSignal(dict)
    on_address = pyqtSignal(dict)

    def __init__(self, parent, account, http_proxy_host=None, http_proxy_port=None):
        QThread.__init__(self, parent)
        self.listener = Listener(account,
                                 on_push=self.on_push,
                                 http_proxy_host=http_proxy_host,
                                 http_proxy_port=http_proxy_port)
        self._account = account
        self.last_pushes_date = None

    def on_push(self, notif_push):
        if notif_push['type'] == 'tickle':
            success, pushes = self._account.get_pushes(modified_after=str(self.last_pushes_date))
            for push in pushes:
                if 'type' in push:
                    if push['type'] == 'link':
                        self.on_link.emit(push)
                    if push['type'] == 'address':
                        self.on_address.emit(push)
                    if push['type'] == 'note':
                        self.on_note.emit(push)
                    if push['type'] == 'list':
                        self.on_list.emit(push)
                    if push['type'] == 'file':
                        self.on_file.emit(push)
                    self.last_pushes_date = push['modified']

    def run(self):
        self.last_pushes_date = time.time()
        self.listener.run_forever()

    def quit(self):
        try:
            self.listener.close()
        except Exception:
            pass
        QThread.quit(self)
