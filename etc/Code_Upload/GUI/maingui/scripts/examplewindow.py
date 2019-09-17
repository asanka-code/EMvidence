# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qtproject/examplewindow.ui',
# licensing of 'Qtproject/examplewindow.ui' applies.
#
# Created: Tue May  7 17:56:23 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ExampleWindow(object):
    def setupUi(self, ExampleWindow):
        ExampleWindow.setObjectName("ExampleWindow")
        ExampleWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ExampleWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setObjectName("widget")
        self.tableView = QtWidgets.QTableView(self.widget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 256, 192))
        self.tableView.setObjectName("tableView")
        self.upload_date = QtWidgets.QDateTimeEdit(self.widget)
        self.upload_date.setGeometry(QtCore.QRect(310, 30, 199, 27))
        self.upload_date.setObjectName("upload_date")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(430, 60, 80, 26))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        ExampleWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ExampleWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        ExampleWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ExampleWindow)
        self.statusbar.setObjectName("statusbar")
        ExampleWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ExampleWindow)
        QtCore.QMetaObject.connectSlotsByName(ExampleWindow)

    def retranslateUi(self, ExampleWindow):
        ExampleWindow.setWindowTitle(QtWidgets.QApplication.translate("ExampleWindow", "MainWindow", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("ExampleWindow", "GroupBox", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("ExampleWindow", "PushButton", None, -1))

