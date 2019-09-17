#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `uctest` package."""
import sys

sys.path.append("..")  # Adds higher directory to python modules path.
import pytest
from uctest import UCTest


@pytest.fixture
def uc_connection():
    return UCTest("COM2")


def test_content(uc_connection):
    assert uc_connection.get_comport() == "COM2"
