__version__ = '0.1.0'
from functools import partial
import sys
from PySide2 import QtWidgets
from uctest.UCTest import ADUCM4050, Leonardo, UCTest
from uctest.UCGUI.mainwindow import Ui_MainWindow


class UCGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UCGUI, self).__init__()

        # UI Setup
        self.ui = Ui_MainWindow()
        # self.ui.tabIdentification.setFocus()
        self.ui.setupUi(self)
        self.setup_ui()

        # UC Device
        self.device = None  # type:UCTest

    def setup_ui(self):
        self.setWindowTitle("UC Test GUI v" + str(__version__))
        self.ui.pb_connect.clicked.connect(self.connect_device)

    def setup_uc_commands(self):
        """
        For the loaded self.device, create buttons for the functions in it's
        internal _function_dicts
        :return: None
        """
        # Loop over all command/function dictionaries
        for ftable in self.device._function_dicts:
            # Create buttons and connect to function disptacher for each entry
            for cmd_name in ftable:
                # Create a Push button and place in the scroll area
                new_pb = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
                new_pb.setObjectName(f"pb_gen_{cmd_name}")
                new_pb.setText(cmd_name)
                self.ui.verticalLayout_3.addWidget(new_pb)
                # Create a function and connect
                new_pb.clicked.connect(partial(self.run_command, cmd_name))

    def run_command(self, command_name):
        """
        Function dipatcher. Run the named command, adding paramters from UI elements
        :param command_name: Name of command in self.device (taken from function table)
        :return:
        """
        # Command Name
        device_method = getattr(self.device, command_name)

        # Read the settings from the UI:
        self.device._comport = self.ui.le_comport.text()
        repeat = self.ui.sb_runs.value()
        if self.ui.cb_runs_forever.isChecked():
            repeat = 0
        duration = self.ui.sb_duration.value()

        # Run command
        device_method(repeat=repeat, duration=duration)

    def connect_device(self) -> bool:

        # Select DUT based on UI checkboxes
        comport = self.ui.le_comport.text()
        if self.ui.rb_cog4050.isChecked():
            self.device = ADUCM4050(comport=comport)
            self.setup_uc_commands()  # Load commands from plugin directory
            self.ui.pb_connect.clicked.connect(self.device.connect)
        if self.ui.rb_leonardo.isChecked():
            self.device = Leonardo(comport=comport)
            self.setup_uc_commands()  # Load commands from plugin directory

        # Connect, showing error message if there is a problem
        if not self.device.connect():
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Error")
            box.setText("Could not connect to device.")
            box.setInformativeText("Please check the COM Port")
            box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            box.setDefaultButton(QtWidgets.QMessageBox.Ok)
            box.exec_()
            return False

        return True


def main():
    """
    Run main Qt GUI
    :return: None
    """
    app = QtWidgets.QApplication([])
    application = UCGUI()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
