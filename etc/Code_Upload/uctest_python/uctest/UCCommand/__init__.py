# -*- coding: utf-8 -*-

import logging
from typing import List, Union

import crcmod

logger = logging.getLogger(__name__)

"""Main module."""


def crc16_ccitt(bytes_in: bytearray):
    crc16 = crcmod.predefined.Crc('xmodem')
    crc16.update(bytes_in)

    return crc16.digest()


def convert_bytearray(some_input: Union[bytearray, bytes, str, List[int]]) -> bytearray:
    """
    Take input in form og bytearrat, string, bytes or list of ints and return bytearrat
    :param some_input:
    :return:
    """
    output_bytearray = bytearray()

    # Parse supplied payload
    if type(some_input) == bytearray:
        output_bytearray = some_input
    elif type(some_input) == str:
        output_bytearray = bytearray(some_input.encode("ASCII"))
    elif type(some_input) == list:
        if type(some_input[0]) == int:
            output_bytearray = bytearray(some_input)
        else:
            RuntimeError("Unsupported conversion")
    elif type(some_input) == bytes:
        output_bytearray = bytearray(some_input)

    return output_bytearray


PACKET_HEADER = 4


class UCCommand:
    """
    Class wrapping bytes send to UC over serial.
    Data is stored in _payload which can be appended or replaced.
    packet returns the pacakged data with header information (length and crc) added
    """

    def __init__(self, payload: Union[bytearray, bytes, str, List[int]]):
        self._payload = convert_bytearray(payload)  # Bytes send to UC
        self._crc = 0
        self._packet = bytes()

    def generate_packet(self):
        """
        Generate the packet of bytes to be send over Serial, adding length and crc
        :return:
        """
        bytes_len = len(self._payload) + 4 # Does not include Header
        bytes_len_low = (bytes_len & 0xFF)
        bytes_len_high = ((bytes_len >> 8) & 0xFF)
        self._crc = crc16_ccitt(self._payload)
        self._packet = bytes([bytes_len_high, bytes_len_low]) + self._crc + self._payload

    @property
    def packet(self) -> bytes:
        """
        Return full command packet with Header (Length and CRC)
        :return: Command packet bytearray
        """
        self.generate_packet()
        return self._packet

    @property
    def crc(self) -> int:
        self.generate_packet()
        return (self._crc[0] << 8) + self._crc[1]

    def __str__(self):
        """
        Return string version of class, i.e. Hex encoded payload data
        :return:
        """
        return "0x" + self.packet.hex().upper()

    def __eq__(self, other):
        return self._payload == other._payload

    def __add__(self, other):
        self._payload = self._payload + convert_bytearray(other)
        return self

    def __len__(self):
        return len(self.packet)

    def append(self, other):
        self._payload = self._payload + convert_bytearray(other._payload)
