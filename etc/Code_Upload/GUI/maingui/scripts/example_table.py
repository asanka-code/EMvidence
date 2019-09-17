import sys

import matplotlib
from datetime import datetime

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PySide2 import QtCore, QtWidgets, QtGui
from scripts.examplewindow import Ui_ExampleWindow
from PySide2.QtCore import QDate, QTime
from PySide2.QtWidgets import QMessageBox


def create_model_from_dict(model_list, parent=None) -> QtGui.QStandardItemModel:
    """
    Use to populate listview in table
    :param model_list: List of dicts for each row
    :param parent: Parent of model
    :return:
    """
    model = QtGui.QStandardItemModel(0, 3, parent)
    for m in model_list:
        model.invisibleRootItem().appendRow([
            QtGui.QStandardItem(m['desc']),
            QtGui.QStandardItem(m['owner']),
            QtGui.QStandardItem(m['created']),
            # QtGui.QStandardItem(m['uuid'])
        ])
    return model


class MainGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainGUI, self).__init__()
        self.ui = Ui_ExampleWindow()
        self.ui.setupUi(self)

        web_dict = [{"desc": "Desc A", "owner": "Bob", "created": "123"},
                    {"desc": "Desc B", "owner": "Alice", "created": "456"},
                    {"desc": "Desc C", "owner": "Bob", "created": "789"}]

        parts_model = create_model_from_dict(web_dict, self)
        parts_model.setHorizontalHeaderLabels(["Signal Name", "Uploaded", "Created"])
        self.ui.tableView.setModel(parts_model)
        self.ui.pushButton.clicked.connect(self.getDate)
        self.ui.upload_date.setDate(QDate.currentDate())
        self.ui.upload_date.setTime(QTime.currentTime())

        # self.ui.upload_date.setDisplayFormat("YYYY-MM-DD")  # 2019-04-23T17:50:50.480587Z

    def getDate(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Error")
        msgBox.setText("There was an error connecting to the web storage server.")
        msgBox.setInformativeText("Check your login credentials.")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setIcon(QMessageBox.Warning)
        ret = msgBox.exec_()

        x = datetime.isoformat(datetime.utcnow()) + 'Z'
        print(x)
        dt = self.ui.upload_date.dateTime()
        x = self.ui.upload_date.dateTime().toString(QtCore.Qt.ISODate)
        print(x)
        # print(self.ui.upload_date.textFromDateTime (dt))


def main():
    """
    Run main Qt GUI
    :return: None
    """
    app = QtWidgets.QApplication([])
    application = MainGUI()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
