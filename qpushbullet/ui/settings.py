# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/settings.ui'
#
# Created: Fri Aug 15 08:12:52 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(400, 194)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/logo32")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Settings.setWindowIcon(icon)
        self.gridLayout_3 = QtGui.QGridLayout(Settings)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox = QtGui.QGroupBox(Settings)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.api_edt = QtGui.QLineEdit(self.groupBox)
        self.api_edt.setObjectName(_fromUtf8("api_edt"))
        self.gridLayout.addWidget(self.api_edt, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 2)
        self.groupBox_2 = QtGui.QGroupBox(Settings)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.proxy_host_edt = QtGui.QLineEdit(self.groupBox_2)
        self.proxy_host_edt.setObjectName(_fromUtf8("proxy_host_edt"))
        self.gridLayout_2.addWidget(self.proxy_host_edt, 0, 0, 1, 1)
        self.proxy_port_edt = QtGui.QLineEdit(self.groupBox_2)
        self.proxy_port_edt.setMaxLength(4)
        self.proxy_port_edt.setObjectName(_fromUtf8("proxy_port_edt"))
        self.gridLayout_2.addWidget(self.proxy_port_edt, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(121, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "QPushDialog Settings", None))
        self.groupBox.setTitle(_translate("Settings", "Pushbullet Api Key", None))
        self.groupBox_2.setTitle(_translate("Settings", "HTTP Proxy", None))
        self.proxy_host_edt.setPlaceholderText(_translate("Settings", "Hostname", None))
        self.proxy_port_edt.setInputMask(_translate("Settings", "Dddd", None))
        self.proxy_port_edt.setPlaceholderText(_translate("Settings", "Port", None))

import qpushbullet.resources_rc
