__version__ = '0.1.0'
import argparse
import json
import os
import sys

# PDF file handling
from PySide2.QtWidgets import QFileDialog  # For saving file
from tempfile import mkstemp, NamedTemporaryFile
from shutil import copyfile

from loguru import logger
from maingui.mainwindow import Ui_MainWindow
from maingui.logindialog import Ui_LoginDialog
from PySide2 import QtWidgets, QtGui, QtCore
from pathlib import Path
from maingui.partfinder import PartFinder
from maingui.settings import AppSettings, ServerLoginDetails
from typing import Optional

# Report Tab Preview
from maingui.report_generation import Report, ReportTypes
from urllib.parse import quote  # For URL path
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtCore import QUrl
from PySide2.QtCore import QDate, QTime

# Storage
from sigmf.sigmffile import SigMFFile
from sigmf.sigmf_hash import calculate_sha512
import numpy as np
from PySide2.QtWidgets import QMessageBox

# Analysis Tab
from maingui.WebStorage import WebStorage

# Capture Tab
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from maingui.RFSource import RadioHW, RFCaptureThread, RFSource


# Helper functions

def shape_input(input_data):
    """
    TGemp function, may be overwrriten by data from server
    :param input_data:
    :return:
    """
    pass

def create_model_from_dict(elist: dict, parent=None) -> QtGui.QStandardItemModel:
    """
    Use to populate listview in table
    :param elist:
    :param parent:
    :return:
    """
    model = QtGui.QStandardItemModel(0, 2, parent)
    for e in elist:
        it = QtGui.QStandardItem(e)
        model.appendRow(it)
    return model


def get_pdf_view_url(path_to_pdf: str, relative: bool = False) -> str:
    """
    Return a URL to display the selected PDF in a browser. Can be realtive to GUI exe.
    :param path_to_pdf: Path to PDF
    :param relative: Make URL relative to GUI?
    :return: str
    """

    current_path = os.path.dirname(__file__)   # Current path, used to get location of viewer.html
    if relative:
        report_pdf = quote(f"file://{current_path}/{path_to_pdf}")
    else:
        report_pdf = quote(f"file://{path_to_pdf}")

    viewer_url = f"file://{current_path}/report_preview/web/viewer.html?file={report_pdf}"
    return viewer_url


class LoginDialog(QtWidgets.QDialog):
    """
    Dialog to get web back-end login details
    """

    def __init__(self, serversettings=ServerLoginDetails):
        super(LoginDialog, self).__init__()
        self.ui = Ui_LoginDialog()
        # self.ui.tabIdentification.setFocus()
        self.ui.setupUi(self)
        self.ui.le_server.setText(serversettings.server)
        self.ui.le_username.setText(serversettings.username)


# Plot GUI
class MatplotlibCanvas(FigureCanvas):
    """
    Embed a Matplotlib plot, based on Matplotlib Example:
    https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100, ):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Set Defaults
        self.data = None
        self.sample_rate = 000

        # Timer to update data
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(5000)

    def update_data(self, data, sample_rate):
        logger.info("Update MatplotlibCanvas Data")
        self.data = data
        self.sample_rate = sample_rate

    def update_figure(self):
        logger.info("Update MatplotlibCanvas Figure")
        if self.data is not None:
            self.axes.cla()
            self.axes.psd(self.data, NFFT=1024, Fs=self.sample_rate)
            self.draw()


# Main Applciation
class MainGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainGUI, self).__init__()

        # Load settings
        self._appsettings = AppSettings()
        self.partfinder = PartFinder()

        # Configure Logging
        logger.add(Path(self._appsettings.config_path, "log_{time}.log"))
        logger.info("Load UI")

        # Configuration
        self._logindetails = ServerLoginDetails()
        # Load Server Settings
        self._logindetails = self._appsettings.read_server_settings()

        # State data for Part Identification
        self.lv_parts_model = None  # type: Optional[QtGui.QStandardItemModel]  # Model loaded from DB
        self.idn_images = []  # List of images for IDN tab
        self.idn_image_index = 0  # Index of currently displayed image
        self.generated_report = None  # Last generated report

        # UI Setup
        self.ui = Ui_MainWindow()
        # self.ui.tabIdentification.setFocus()
        self.ui.setupUi(self)
        self.setup_ui()
        self.idn_images_update()

        # Triggering
        self.rfcapture = None  # type: RFCaptureThread

        # Capture Tab
        logger.info("Embed matplotlib canvas for Signal Preview")
        self._capture_preview_canvas = MatplotlibCanvas(self.ui.frame_4, width=500, height=400, dpi=100)
        self.ui.gridLayout_9.addWidget(self._capture_preview_canvas)

        # Analysis
        self.webstorage = None  # type: WebStorage  # Interface to RF records Server
        self._classifiers = None  # type: dict  # Local or remote classifier details
        self._signals = None  # type: dict  # Local or remote RF records
        self.rfdata = None  # type: np.array  # RF data loaded from server or from SDR
        self._ml = None  # type: dict  # Local download of ML model {"type": "kera", "location": "/tmp/abcdef", "name": "ECC detection"}
        if self._logindetails.server:  # If details saved, update Webstorage details
            self.webstorage = WebStorage(self._logindetails.server)

        # Emdedded Webpage for Report Preview
        self.page = QWebEnginePage()
        self.page.profile().clearHttpCache()
        self.ui.web_report_preview.setPage(self.page)
        self.preview_report("report_preview/default.pdf", True)

    def preview_report(self, report_location: str, relative_location: bool = False) -> None:
        """
        Display the PDF report in the UI
        :param relative_location:  Is PDF location relative to GUI exe?
        :param report_location: Location of PDF
        :return:
        """
        pdf_url = get_pdf_view_url(report_location, relative_location)
        logger.info(f"Previewing {pdf_url}")
        self.ui.web_report_preview.load(QUrl(pdf_url))
        self.ui.web_report_preview.show()

    def setup_ui(self):
        """
        Set up the main GUI, connecting buttons and populating defaults
        :return:
        """
        # Default values
        self.ui.pb_nextIDN.setEnabled(False)
        self.setWindowTitle("RF Forensics Tool v" + str(__version__))
        # Connect up buttons and actions
        self.ui.te_partialIDN.textChanged.connect(self.identify_part)
        # Menus
        self.ui.action_Login.triggered.connect(self.login)
        self.ui.action_Exit.triggered.connect(self.close)
        # Image
        self.ui.pb_IDNnext.clicked.connect(self.idn_image_next)
        self.ui.pb_IDNprevious.clicked.connect(self.idn_image_prev)
        self.ui.pb_nextIDN.clicked.connect(self.load_identity_from_list)
        self.ui.pb_selectIDN.clicked.connect(self.load_identity_from_images)

        # Capture Tab
        hardware_backends = [e.value for e in RadioHW]
        for i, t in enumerate(hardware_backends):  # Add options to ComboBox
            self.ui.cb_capture_hw.insertItems(i, [t])
        self.ui.pb_capture_trigger.clicked.connect(self.trigger_capture)

        # Storage Tab
        self.ui.pb_storage_upload.clicked.connect(self.storage_upload)
        self.ui.pb_storage_savelocal.clicked.connect(self.storage_savelocal)
        self.ui.pb_storage_update.clicked.connect(self.storage_update_from_server)
        self.ui.pb_storage_load.clicked.connect(self.storage_load)
        self.ui.cb_upload_datatype.insertItems(0, ["cf32"])
        self.ui.upload_date.setDate(QDate.currentDate())
        self.ui.upload_date.setTime(QTime.currentTime())

        # Analysis Tab
        self.ui.pb_analysis_load.clicked.connect(self.analysis_load_models)
        self.ui.pb_analysis_run.clicked.connect(self.run_analysis)

        # Report Generation
        self.ui.pb_save_report.clicked.connect(self.report_save)
        self.ui.pb_report_generate.clicked.connect(self.report_generate)
        report_types = ReportTypes.keys()
        for i, t in enumerate(report_types):  # Add options to ComboBox
            self.ui.cb_report_template.insertItems(i, [t])

    def idn_images_update(self):
        """
        Update the list of images to show on the IDN tab from the loaded DB
        :return: None
        """
        logger.info(f"Load {len(self.partfinder.partdb)} images from DB.")
        self.idn_image_index = 0  # Reset Image index
        maingui_path = os.path.dirname(__file__)
        for board in self.partfinder.partdb:
            self.idn_images.append(f"{maingui_path}/database/" + self.partfinder.partdb[board]["Image"])

        self.idn_set_image()

    def idn_set_image(self, index: Optional[int] = None):
        """
        Set the IDN image to the selected index
        :param index:
        :return: None
        """
        if not index:
            index = self.idn_image_index
        logger.info(f"Setting IDN image to [{self.idn_image_index}]: {self.idn_images[index]}")
        idn_image_pixmap = QtGui.QPixmap(self.idn_images[index])
        idn_scaled_pixmap = idn_image_pixmap.scaled(self.ui.label_idn_image.size(), QtCore.Qt.KeepAspectRatio)
        self.ui.label_idn_image.setPixmap(idn_scaled_pixmap)
        self.idn_image_index = index

    def idn_image_next(self):
        """
        Show the next IDN image, looping if neccessary
        :return:
        """
        if self.idn_image_index == len(self.idn_images) - 1:
            self.idn_image_index = 0
        else:
            self.idn_image_index += 1
        self.idn_set_image()

    def idn_image_prev(self):
        """
        Show the previous IDN image, looping if neccessary
        :return:
        """
        if self.idn_image_index == 0:
            self.idn_image_index = len(self.idn_images) - 1
        else:
            self.idn_image_index -= 1
        self.idn_set_image()

    def identify_part(self):
        """
        Initiliase the table to help identify parts, populating the table from the part finder
        :return:
        """
        self.ui.pb_nextIDN.setEnabled(True)
        part_dict = self.partfinder.process_partname(self.ui.te_partialIDN.toPlainText())
        self.lv_parts_model = create_model_from_dict(part_dict, self)
        self.ui.lv_parts.setModel(self.lv_parts_model)

    def load_identity_from_list(self):
        """
        Use the currently selected row in the Parts table to identify the part/board
        :return:
        """
        idx = self.ui.lv_parts.selectedIndexes()[0]
        board_selected = self.lv_parts_model.itemFromIndex(idx).text()
        logger.info(f"board_selected: {board_selected}")
        self.set_recommended_paramters(board_selected)
        self.ui.tabCenter.setCurrentIndex(1)

    def load_identity_from_images(self):
        """
        Use the currently open image to identify the board/part
        :return:
        """
        idx = self.idn_image_index
        board_selected = list(self.partfinder.partdb)[idx]
        logger.info(f"board_selected: {board_selected}")
        self.set_recommended_paramters(board_selected)
        self.ui.tabCenter.setCurrentIndex(1)

    def set_recommended_paramters(self, board_name: str):
        """
        Update the UI with the recommended parameters for board_name
        :param board_name: String of board/part in database
        :return:
        """
        board_selected = self.partfinder.find(board_name)
        # Set recommended setttings
        self.ui.te_capture_freq.setPlainText(board_selected["Freq"])
        self.ui.te_capture_span.setPlainText(board_selected["Span"])
        self.ui.te_capture_sampling.setPlainText(board_selected["Sampling"])
        # Set the chosen settings to recommended by default
        self.ui.te_settings_freq.setPlainText(board_selected["Freq"])
        self.ui.te_settings_span.setPlainText(board_selected["Span"])
        self.ui.te_settings_sampling.setPlainText(board_selected["Sampling"])

    def trigger_capture(self):
        """
        Trigger a capture from the HW backend
        :return:
        """
        logger.info("Trigger Capture")
        # Read settings from UI
        window_size = int(self.ui.sb_capture_length.value())
        trigger_delay = int(self.ui.sb_capture_trigger_delay.value())
        radiobackend_idx = self.ui.cb_capture_hw.currentIndex()
        radiobackend = RadioHW([e for e in RadioHW][radiobackend_idx])
        logger.info(f"window_size: {window_size}")
        logger.info(f"trigger_delay: {trigger_delay}")
        logger.info(f"radiobackend: {radiobackend}")

        # Start capture thread
        rfsource = RFSource()
        freq = float(self.ui.te_settings_freq.toPlainText().lower().rstrip("mhz")) * 1e6  # MHz to Hz
        sample_rate = float(self.ui.te_settings_sampling.toPlainText().lower().rstrip("k")) * 1e3  # kHz to Hz
        rfsource.configure_radio(radiobackend, freq, sample_rate)
        self.rfcapture = RFCaptureThread(rfsource, parent=self, callback="capture_complete_cb", delay_s=trigger_delay)
        self.rfcapture.start()

    def capture_complete_cb(self):
        """
        Callback when RF capture has been completed
        :return:
        """
        logger.info("capture_complete_cb")
        self.rfdata = self.rfcapture.rfsource.rfdata
        sample_rate = self.rfcapture.rfsource._radio_sampling_rate
        self._capture_preview_canvas.update_data(self.rfdata, sample_rate)

    def login(self):
        """
        Show the Login Dialog and save the username and password
        :return:
        """
        serverdialog = LoginDialog(self._logindetails)
        # Get info if "OK" pressed
        if serverdialog.exec_():
            self._logindetails.server = serverdialog.ui.le_server.text()
            self._logindetails.username = serverdialog.ui.le_username.text()
            self._logindetails.password = serverdialog.ui.le_password.text()
            self._appsettings.write_server_settings(self._logindetails)

            self.webstorage = WebStorage(self._logindetails.server)
            self.webstorage.login_details(self._logindetails.username, self._logindetails.password)

    def analysis_load_models(self):
        """
        Load ML models from local hard drive or from web backend
        :return:
        """
        success, classifiers = self.webstorage.get_classifiers()
        if success:
            self._classifiers = classifiers
            self.analysis_update_table()
        else:
            self.show_storage_error()
            logger.info("Failed to load Classifier list from web backend")

    def analysis_update_table(self):
        """
        Update the Analysis table
        :return:
        """
        if self._classifiers:
            model = QtGui.QStandardItemModel(0, 4, self)
            model.setHorizontalHeaderLabels(["Classifier", "Uploader", "Description", "Machine Learning Model"])
            for m in self._classifiers:
                model.invisibleRootItem().appendRow([
                    QtGui.QStandardItem(m['name']),
                    QtGui.QStandardItem(m['owner']),
                    QtGui.QStandardItem(m['description']),
                    QtGui.QStandardItem(m['ml'])
                ])
            self.ui.tb_analysis_classifiers.setModel(model)
            self.ui.tb_analysis_classifiers.setVisible(False)
            self.ui.tb_analysis_classifiers.resizeColumnsToContents()
            self.ui.tb_analysis_classifiers.setVisible(True)

    def run_analysis(self):
        """
        Use the selected Classifier on the currently loaded data
        :return:
        """
        self.load_classifier()

        # Only run if Data loaded
        if self.rfdata is None:
            self.show_not_configured_warning("RF data not available for upload.")
            return

        input_data = self.rfdata

        # Process data based on ML backend
        if self._ml['type'] == 'Keras':  # PyTorch
            from tensorflow.python.keras.models import load_model
            model = load_model(self._ml['location'])

            if len(self._ml['data_preprocess']) == 0 or self._ml['data_preprocess'] == "None":
                # Default data processing, based on colloration with Asanka S.
                from classifiers import sample_data_sliding_window
                processed_data = sample_data_sliding_window(input_data)

                input_data = np.array([processed_data]) # Reshape for classifier
            else:
                # Load function from ML metadata and use it to post-process the data
                exec(self._ml['data_preprocess'])
                input_data = shape_input(input_data)
            scores = model.predict(input_data)

            score_label = self._ml['score_labels'].split(';')[1]
            self._ml['results'] = f"{self._ml['name']}\nResult: {score_label} {scores[0][0]}"
            self.ui.te_analysis_results.setText(self._ml['results'])
            self.ui.te_report_details.setText(self._ml['results'])

    def load_classifier(self):
        """
        Load the selected Classifier and store the data locally
        :return:
        """
        idx = self.ui.tb_analysis_classifiers.selectedIndexes()[0]
        logger.info(f"Run Analysis: {idx.row()}")
        classifier_selected = self._classifiers[idx.row()]
        logger.info(classifier_selected)
        uuid = classifier_selected['uuid']
        temp_classifier = self.webstorage.download_classifier(uuid)

        # Reset current loaded ML
        self._ml = {"name": classifier_selected['name'], "location": temp_classifier, "type": classifier_selected['ml'],
                    "score_labels": classifier_selected['score_labels'],
                    "data_preprocess": classifier_selected['data_preprocess']}
        logger.info(self._ml)

    def storage_update_from_server(self):
        """
        Load saved RF signals from Web backend
        :return:
        """
        success, signals = self.webstorage.get_signals()
        if success:
            logger.info("Load RF signal list from web backend")
            self._signals = signals

            model = QtGui.QStandardItemModel(0, 4, self)
            model.setHorizontalHeaderLabels(["Signal Name", "Uploader", "Created", "UUID"])
            for m in signals:
                model.invisibleRootItem().appendRow([
                    QtGui.QStandardItem(m['core_description']),
                    QtGui.QStandardItem(m['owner']),
                    QtGui.QStandardItem(m['created']),
                    QtGui.QStandardItem(m['uuid'])
                ])
            self.ui.tv_storage.setModel(model)
            self.ui.tv_storage.setVisible(False)
            self.ui.tv_storage.resizeColumnsToContents()
            self.ui.tv_storage.setVisible(True)
        else:
            self.show_storage_error()
            logger.info("Failed to load RF signal list from web backend")

    def storage_savelocal(self):
        """
        Save the RF signal and metadata locally
        :return:
        """
        self.storage_save(local=True)

    def storage_upload(self):
        """
        Upload current data to the server with the SigMF data from the UI
        :return:
        """
        self.storage_save(local=False)

    def storage_save(self, local: bool = True):
        """
        Save current data with the SigMF data from the UI locally or to the server
        :param local: Save data locally? If false, try to save to remote server if conncted
        :return:
        """
        # Reading settings from UI
        sig_time = self.ui.upload_date.dateTime().toString(QtCore.Qt.ISODate)
        sig_desciption = self.ui.pt_upload_name.toPlainText()
        sig_author = self.ui.le_upload_author.text()
        sig_licence = self.ui.le_upload_licence.text()
        sig_datatype = self.ui.cb_upload_datatype.currentText()
        sig_version = self.ui.le_upload_version.text()
        sig_tags = self.ui.le_upload_tags.text().split(",")

        if self.rfdata is None:
            self.show_not_configured_warning("RF data not available for upload.")
            return

        # Save rfdata to file and get hash
        temp_file = NamedTemporaryFile(delete=False)
        logger.info(f"Save RF data to temporary file {temp_file.name}")
        np.save(temp_file, self.rfdata)
        np.save(temp_file, self.rfdata)
        file_sha = calculate_sha512(temp_file.name)
        logger.info(f"RF data SHA: {file_sha}")

        # Construct SigMF and uploads
        _, sample_metafile = mkstemp()
        sample_capture1 = {'core:sample_start': 0}
        sample_annotation1 = {'core:sample_count': 16, 'core:sample_start': 0}
        metadata = {"global":
                        {"core:version": sig_version, 'core:datatype': sig_datatype, 'core:description': sig_desciption,
                         "core:sha512": file_sha, "core:hw": self.ui.cb_capture_hw.currentText(),
                         "core:author": sig_author,
                         "core:license": sig_licence},
                    "captures": [sample_capture1], "annotations": [sample_annotation1]}
        # Save metadata to file

        # Validate
        signal1 = SigMFFile(metadata=metadata, data_file=temp_file.name)
        logger.info(signal1)
        logger.info("Validation Passed") if signal1.validate() else logger.info("Validation Failed")

        if local:
            save_filename, _ = QFileDialog.getSaveFileName(self, "SigMF Metadata", "", "SigMF Metadata(*.sigmf-meta)")

            with open(save_filename + ".sigmf-meta", 'w') as outfile:
                json.dump(metadata, outfile)
            with open(save_filename + ".sigmf-data", 'wb') as outfile:
                np.save(outfile, self.rfdata)
        else:
            # Upload data
            if self.webstorage.upload_signal(metadata, temp_file.name) is not None:
                logger.info("Successfully uploaded Signal")

    def storage_load(self):
        """
        Load the selected RF Signal from the Server
        :return:
        """
        # Get the UUID of the selected signal
        idx = self.ui.tv_storage.selectedIndexes()[0]
        logger.info(f"Load storage: {idx.row()}")
        signal_selected = self._signals[idx.row()]
        logger.info(signal_selected)
        uuid = signal_selected['uuid']
        temp_signal_record = self.webstorage.download_signal(uuid)
        self.rfdata = np.load(temp_signal_record)  # Override last captured signal

    def show_storage_error(self):
        """
        Show a message box if there is a problem connecting to the server.
        :return:
        """
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Error")
        msgBox.setText("There was an error connecting to the web storage server.")
        msgBox.setInformativeText("Check your login credentials.")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setIcon(QMessageBox.Warning)
        ret = msgBox.exec_()

    def show_not_configured_warning(self, message:str):
        """
        Show a message box if the GUI is not configured correctly
        :return:
        """
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Error")
        msgBox.setText("Cofiguration Error")
        msgBox.setInformativeText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setIcon(QMessageBox.Warning)
        ret = msgBox.exec_()

    def report_save(self):
        """
        Save the last generated PDF
        :return:
        """

        report_filename, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "PDF (*.pdf)")

        if report_filename and self.generated_report:
            copyfile(self.generated_report, report_filename)
            logger.info(f"Copied {self.generated_report} to {report_filename}")

    def report_generate(self):
        """
        Generate a report using the selection template from the dropdown
        Create temporary PDF file and preview
        :return: None
        """

        # Create the Report data object
        report = Report()
        report.technician = self.ui.le_report_technician.text()
        report.date = self.ui.le_report_date.text()
        report.location = self.ui.le_report_location.text()
        report.report_id = self.ui.le_report_id.text()
        report.details = self.ui.te_report_details.toPlainText()
        report.signoff = self.ui.le_report_signoff.text()

        # Get the selected template from the GUI
        selected_index = self.ui.cb_report_template.currentIndex()
        ReportClass = ReportTypes[self.ui.cb_report_template.itemText(selected_index)]

        # Generate a temporary file
        _, self.generated_report = mkstemp()
        logger.info(f"Create temp file {self.generated_report}")
        rg = ReportClass(report, self.generated_report)
        rg.generate_report()

        # Preview in UI
        self.preview_report(self.generated_report)


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
    # CLI arg handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', help="Enable logging to stdout and log file.", action='store_true', required=False)
    args = parser.parse_args()
    if not args.logging:
        logger.remove()

    # Call
    main()
