#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `uctest` package."""
import sys

sys.path.append("..")  # Adds higher directory to python modules path.
import pytest
from uctest import UCCommand


@pytest.fixture(params=["abcd", [97, 98, 99, 100], bytearray([97, 98, 99, 100])], ids=["str", "list", "bytearray"])
def uccommand_instance(request):
    return UCCommand(request.param)


def test_uccommand(uccommand_instance):
    assert uccommand_instance.crc == 43062
    assert len(uccommand_instance) == 8
    assert uccommand_instance.packet == bytearray([0, 8, 0xA8, 0x36, 97, 98, 99, 100])
    assert str(uccommand_instance) == "0x0008A83661626364"


def test_uccommand_append(uccommand_instance):
    uccommand_other = UCCommand("efgh")
    uccommand_instance.append(uccommand_other)
    assert uccommand_instance.crc == 44031
    assert len(uccommand_instance) == 12
    assert uccommand_instance.packet == bytearray([0, 12, 0xAB, 0xFF, 97, 98, 99, 100, 101, 102, 103, 104])
    assert str(uccommand_instance) == "0x000CABFF6162636465666768"


def test_uccommand_eq(uccommand_instance):
    another_instance = UCCommand("abcd")
    assert another_instance == uccommand_instance
