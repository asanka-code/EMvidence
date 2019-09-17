
from PySide2 import QtCore, QtWidgets, QtGui

class MainGUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)
        self.centralwidget = QtGui.QWidget(self)
        self.view = QtGui.QTableView(self.centralwidget)
        self.view.setSortingEnabled(True)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.addWidget(self.view, 1, 0, 1, 3)

        self.setCentralWidget(self.centralwidget)

        self.model = QtGui.QStandardItemModel(self)

        for rowName in range(3) * 5:
            self.model.invisibleRootItem().appendRow(
                [QtGui.QStandardItem("row {0} col {1}".format(rowName, column))
                 for column in range(3)
                 ]
            )
        for column in range(3):
            self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                                     'Column %d' % int(column + 1))
            for row in range(3 * 5):
                self.model.setHeaderData(row, QtCore.Qt.Vertical,
                                         'Row %d' % int(row + 1))

        self.proxy = QtGui.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)

        self.view.setModel(self.proxy)


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
