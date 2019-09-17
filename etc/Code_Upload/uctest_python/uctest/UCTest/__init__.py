# -*- coding: utf-8 -*-

import logging
import serial
import sys
import os
import importlib
import time
from typing import List, Union
from uctest.UCCommand import UCCommand
from typing import Optional

logger = logging.getLogger(__name__)

"""Main module."""

CMD_SM_SET_BOARD_ID = 0x501
CMD_SM_GET_BOARD_ID = 0x502

uc_uecc_function_table = {
    "uecc_make_key": 0x3001,
    "uecc_sign": 0x3002,
    "uecc_verify": 0x3003,
}


class UCTest:
    """
    Base Class for Micro-Controller test program
    """

    def __init__(self, comport: str, verbose: bool = False):
        """
        Create a UCTest object
        :param comport: COM port to connect to
        :param verbose: Level of Verbosity, Default: off
        """
        self._verbose = verbose
        self._connected = False  # Connected to uC?
        self._uart_baudrate = 9600
        self._uart_rtsctsdsrdtr = True
        self.msg(f"UC Test Init: {comport}")
        self._comport = comport  # Stores comport location
        self._serial = None  # type: serial.Serial
        self._function_dicts = []  # type: List[dict]  # Stores list of function dictionaries
        self.load_plugins()  # Load plugins

    def load_plugins(self, plugin_dir: str = "../plugins/"):
        """
        Load plugins for a plugin directort
        :param plugin_dir: Path to Plugin dir
        :return: None
        """
        base_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
        plug_abs_dir = base_dir + plugin_dir
        sys.path.append(plug_abs_dir)  # Add to path to use as package

        # Get list of plugins by listing filenames
        plugin_names = [f.rstrip(".py") for f in os.listdir(plug_abs_dir) if f.endswith(".py")]

        # Loop over plugins and add functions
        for plugin_name in plugin_names:
            # Import module
            mod = importlib.import_module(plugin_name, package="plugins")
            ft = getattr(mod, "function_table")
            self.add_functions(ft)  # Add functions to UCTest instance

    def create_uc_function(self, f_name: str, f_parmas: Union[int, dict]):
        """
        Create and return a UC function using a function tempate
        :param f_name: Name of function to create
        :param f_parmas: Function paramaterse, either the command code or a dict of paramaters
        :return:
        """
        if type(f_parmas) == int:
            f_code = f_parmas
        elif type(f_parmas) == dict:
            function_params = f_parmas  # type: dict
            f_code = function_params["command"]
            function_params.pop('command', None)

        def function_template(*args, duration: int = 0, repeat: int = 1, **kwargs):
            self.msg(f"Calling function: {f_name}")
            self.msg(f"     duration: {duration}")
            self.msg(f"     repeat:   {repeat}")

            # Store non default data
            other_parameters = []

            # Loop over values and add to data
            for name, value in kwargs.items():
                self.msg('     {0} = {1}'.format(name, value))
                if type(value) == int:
                    other_parameters.append(value)
                else:
                    other_parameters += value

            code_list = [(f_code >> 8) & 0xFF, (f_code & 0xFF)]
            duration_list = [duration >> 8, duration & 0xFF]
            run_list = [repeat >> 8, repeat & 0xFF]
            self.send((code_list + duration_list + run_list + other_parameters))

        return function_template

    def add_functions(self, fdict: dict) -> None:
        """
        Add functions to UCTest from a dictionary
        Each function has a command identifier byte
        :param fdict:
        :return:
        """
        self.msg(f"Add function: {fdict}")
        self._function_dicts.append(fdict)  # Update internal list of function dicts
        for fname in fdict:
            new_method = self.create_uc_function(fname, fdict[fname])
            setattr(self, fname, new_method)

    def list_functions(self):
        """
        List available UC Functions
        :return: None
        """
        for fdict in self._function_dicts:
            print(f"Functions:\n---------------------------")
            for fentry in fdict:
                print(f"{fentry}: CommandID: 0x{fdict[fentry]:02X}")
            print()

    def get_comport(self):
        return self._comport

    def msg(self, output: str) -> None:
        """
        Log output string. Optionally print to stdout
        :param output: String with information
        :return: None
        """
        logger.info(output)
        if self._verbose:
            print(output)

    def send(self, bytes_to_send):
        command = UCCommand(bytes_to_send)
        if self._connected:
            if self._verbose:
                self.msg(f"Sending ... {command}")
            self._serial.write(command.packet[0:4])
            time.sleep(0.1)
            self._serial.write(command.packet[4:])
        else:
            if self._verbose:
                self.msg(f"Would have Sent ... {command}")

    def receive(self, rx_len: int = 0) -> List[int]:
        if self._connected:
            rx_bytes = self._serial.read_until(size=(rx_len + 4 + 1))  # Header (Len + Cmd) + Err
            rx_bytes_str = [f"{b:02X}" for b in rx_bytes]
            if self._verbose:
                self.msg(f"Receive {rx_len} bytes {rx_bytes_str}")
                if rx_bytes[-1:] != 0:
                    RuntimeError("Last UART Command sent failed CRC.")
            return list(rx_bytes[4:])
        else:
            if self._verbose:
                self.msg(f"Would have Rx'ed {rx_len} bytes")
            return []

    def set_board_id(self, idn: int = 0):
        self.send([CMD_SM_SET_BOARD_ID >> 8, CMD_SM_SET_BOARD_ID & 0xFF, idn >> 8, idn & 0xFF])
        self.receive()

    def get_board_id(self) -> int:
        self.send([CMD_SM_GET_BOARD_ID >> 8, CMD_SM_GET_BOARD_ID & 0xFF])
        idn_array = self.receive(2)
        return (idn_array[0] << 8) + idn_array[1]

    def connect(self, timeout: Optional[int] = 2) -> bool:
        """
        Connect to com port
        :param timeout: UART timeout in seconds, None for no timeout
        :return: Success
        """
        if len(self._comport) > 0:
            try:
                self._serial = serial.Serial(self._comport, self._uart_baudrate, rtscts=self._uart_rtsctsdsrdtr,
                                             dsrdtr=self._uart_rtsctsdsrdtr, timeout=timeout)
            except serial.SerialException as e:
                self.msg(f"[{e}]Cannot connect to {self._comport}")
                return False
            self.msg(f"Connected to {self._comport}")
        else:
            self.msg("Dummy Mode")
        self._connected = True
        return True


class Leonardo(UCTest):

    def __init__(self, comport: str, verbose: bool = False):
        super(Leonardo, self).__init__(comport, verbose)
        self._uart_baudrate = 9600
        self._uart_rtsctsdsrdtr = True

    def reset(self) -> bool:
        pass


class ADUCM4050(UCTest):

    def __init__(self, comport: str, verbose: bool = False):
        super(ADUCM4050, self).__init__(comport, verbose)
        self._uart_baudrate = 115200
        self._uart_rtsctsdsrdtr = False

    def reset(self) -> bool:
        pass


if __name__ == "__main__":
    # Logging
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Test
    # uc = Leonardo("/dev/ttyACM0")
    uc = Leonardo("")
    if uc.connect():
        uc.simple_loop_2(runs=10000)
    else:
        print("Error")
