from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QDialog, QAbstractButton, QDialogButtonBox

from qpushbullet import config
from qpushbullet.ui.settings import Ui_Settings


__author__ = 'Igor Maculan <n3wtron@gmail.com>'


class SettingsDlg(QDialog):

    saved = pyqtSignal()

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.ui.api_edt.setText(config.value('key').toString())
        self.ui.proxy_host_edt.setText(config.value('proxy.host').toString())
        self.ui.proxy_port_edt.setText(config.value('proxy.port').toString())
        self.ui.buttonBox.clicked.connect(self.btn_clicked)


    @pyqtSlot(QAbstractButton)
    def btn_clicked(self, btn):
        if self.ui.buttonBox.standardButton(btn) == QDialogButtonBox.Apply or self.ui.buttonBox.standardButton(btn) == QDialogButtonBox.Save:
            config.setValue('key', self.ui.api_edt.text())
            config.setValue('proxy.host', self.ui.proxy_host_edt.text())
            config.setValue('proxy.port', self.ui.proxy_port_edt.text())
            self.saved.emit()
        self.close()