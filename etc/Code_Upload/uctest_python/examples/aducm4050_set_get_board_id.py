from uctest.UCTest import ADUCM4050
import logging

logger = logging.getLogger(__name__)

dut = ADUCM4050("/dev/ttyACM1", verbose=True)
dut.connect()
dut.set_board_id(0x7890)
idn = dut.get_board_id()
print(f"0x{idn:02X}")
