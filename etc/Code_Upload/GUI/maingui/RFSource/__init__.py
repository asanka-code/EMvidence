"""
This file contains the code requires to start an RF surce for the radio
"""

import os
import time
import zmq
from loguru import logger
import execnet  # MIT Licenced
from enum import Enum
import numpy as np
from threading import Thread
import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


class RadioHW(Enum):
    """
    Support Hardware Backends
    """
    Demo = "RADIO_HW_DEMO"
    HackRFOne = "RADIO_HW_HACKRF_ONE"
    ADIPluto = "RADIO_HW_ADI_PLUTO"


class RFSource:

    def __init__(self, host: str = "127.0.0.1", port: int = 5557):
        """
        Init an RFSource object, creating the ZeroMQ context and socket
        :param host: The ZeroMQ source host, default localhost
        :param port: The ZeroMQ source port, default 5557
        """

        # ZeroMQ Subsciber
        self._zmq_socket = zmq.Context().socket(zmq.SUB)
        self._zmq_source = f"tcp://{host}:{port}"
        logger.info(f"Created RFSource: {self._zmq_source}")

        # Radio data: Demo by default
        self._radio = RadioHW.Demo  # Default to demo mode
        self._radio_frequency = 3e8  # Hz
        self._radio_sampling_rate = 3e6  # Hz

        # Processes for GnuRadio
        self._exec_group = execnet.Group()

        # RF data
        self.rfdata = None  # type: np.array

    def configure_radio(self, radiohw: RadioHW, frequency, sampling):
        """
        Configure the Radio
        :param radiohw: Select the Radio Hardware back-end, from enum
        :param frequency: Center Frequency in Hz
        :param sampling: Sampling Rate in Hz
        :return:
        """
        self._radio = radiohw
        self._radio_frequency = float(frequency)  # Hz
        self._radio_sampling_rate = float(sampling)  # Hz

    def start(self):
        """
        Start subscribing to data
        :return:
        """

        logger.info("Start GnuRadio block")

        """
        Call Python2 process to run GnuRadio code to start data capture
        """
        argument_list = [self._zmq_source, self._radio.value, self._radio_frequency, self._radio_sampling_rate]
        py2_path = os.path.dirname(__file__) + "/RadioInterface"
        logger.info(f"Py2 SYS Path: {py2_path}")
        gw = self._exec_group.makegateway("popen//python=python2")
        channel = gw.remote_exec(f"import sys\n"
                                 f"sys.path.append('{py2_path}')\n"
                                 f"from radio_interface import radio_backend\n"
                                 f"channel.send(radio_backend(*channel.receive()))"
                                 )
        channel.send(argument_list)

        logger.info("Start Subscriber")
        self._zmq_socket.connect(self._zmq_source)
        self._zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all

    def capture(self, window_size: int = 10):
        """
        Capture Data from the RF back-end
        :param window_size: Multiplied by sample rate to get number of samples to be captured
        :return: Temp data file
        """
        logger.info("Capture")
        rfdata_length = int(self._radio_sampling_rate * (window_size * 0.001))
        data_segment = np.empty([0, 0])

        while len(data_segment) < rfdata_length:
            logger.info(f"len(data_segment): {len(data_segment)}")
            radio_data = self._zmq_socket.recv()
            data = np.frombuffer(radio_data, dtype="float32")  # 1D array
            data = data[0::2] + 1j * data[1::2]  # Complex data
            data_segment = np.append(data_segment, data)

        self.rfdata = data_segment[0:rfdata_length]  # Truncate if needed

    def stop(self):
        """
        Stop subscribing
        :return:
        """
        logger.info("Stop Subscriber")
        self._zmq_socket.close()
        logger.info("Stop GnuRadio process")
        self._exec_group.terminate()


class RFCaptureThread(Thread):

    def __init__(self, rfsource: RFSource, parent=None, callback="", delay_s: int = 0):
        """
        A thread to run the RF Capture in the background
        :param rfsource: The RFSource class, handling ZeroMQ connection and data capture
        :param delay_s: Delay before starting the capture
        """
        self.rfsource = rfsource
        self._delay = delay_s
        self._parent = parent
        self._callback = callback
        super(RFCaptureThread, self).__init__()
        self.rfsource.start()

    def run(self):
        time.sleep(self._delay)
        self.rfsource.capture()
        self.rfsource.stop()
        if self._parent:
            getattr(self._parent, self._callback)()
        exit()


if __name__ == "__main__":
    # Quick test to verify it works, using the demo backend, plotting the the FFT
    rf = RFSource()
    sample_rate = 32e6
    rf.configure_radio(RadioHW.Demo, 2e6, sample_rate)

    # rf.start()
    # rf.capture()
    # rf.stop()
    # data = rf.rfdata

    t = RFCaptureThread(rf)
    t.start()
    t.join()
    data = t.rfsource.rfdata
    plt.figure()
    # plot the PSD of the selected sample range of the numpy data array
    plt.psd(data, NFFT=1024, Fs=sample_rate)

    plt.show()
