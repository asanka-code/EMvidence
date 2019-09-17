import sys

import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PySide2 import QtCore, QtWidgets
import random
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from examplewindow import Ui_ExampleWindow


class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)  # type: Axes
        self.x = [1, 2, 3, 4, 5]
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.x = [1, 2, 3, 4, 5]
        # Timer to update data
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [3,4,5,6], 'r')

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class MainGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainGUI, self).__init__()
        self.ui = Ui_ExampleWindow()
        # self.ui.tabIdentification.setFocus()
        self.ui.setupUi(self)
        sc = MyMplCanvas(self.ui.centralwidget, width=5, height=4, dpi=100)
        self.ui.gridLayout.addWidget(sc)
        # self.ui.gridLayout.set
        # self.ui.centralwidget.setCe


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
