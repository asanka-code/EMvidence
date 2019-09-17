# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qtproject/logindialog.ui',
# licensing of 'Qtproject/logindialog.ui' applies.
#
# Created: Tue May  7 17:56:23 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(300, 276)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginDialog.sizePolicy().hasHeightForWidth())
        LoginDialog.setSizePolicy(sizePolicy)
        LoginDialog.setMaximumSize(QtCore.QSize(300, 276))
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(12, 12, 12, 12)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(LoginDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(LoginDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.le_server = QtWidgets.QLineEdit(LoginDialog)
        self.le_server.setObjectName("le_server")
        self.gridLayout.addWidget(self.le_server, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(LoginDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(LoginDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        self.le_username = QtWidgets.QLineEdit(LoginDialog)
        self.le_username.setObjectName("le_username")
        self.gridLayout.addWidget(self.le_username, 4, 1, 1, 1)
        self.le_password = QtWidgets.QLineEdit(LoginDialog)
        self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_password.setObjectName("le_password")
        self.gridLayout.addWidget(self.le_password, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(LoginDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(LoginDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), LoginDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), LoginDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QtWidgets.QApplication.translate("LoginDialog", "Server Login", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("LoginDialog", "Username", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("LoginDialog", "Server Login", None, -1))
        self.le_server.setText(QtWidgets.QApplication.translate("LoginDialog", "http://127.0.0.1:8000", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("LoginDialog", "Password", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("LoginDialog", "Server", None, -1))

