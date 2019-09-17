from uctest.UCTest import ADUCM4050

# Initiliase the device, supplying the port it will connect to
dut = ADUCM4050("/dev/ttyACM0", verbose=True)

# COnnect to the device over serial
dut.connect()

# Give the DUT an ID and print it after reading it back
dut.set_board_id(0x7890)
idn = dut.get_board_id()
print(f"0x{idn:02X}")

# # Run a series of tests

# Run loop 2 once
dut.simple_loop_2()

# RUn loop 2 four times
dut.simple_loop_2(repeat=4)

# Run loop 2 forever
dut.simple_loop_2(repeat=0)

# Run loop 2 continously, but stop after 500 ms
dut.simple_loop_2(repeat=0, duration=500)

# Run uECC on the DUT
dut.uecc_select_curve(curve=1)
dut.uecc_make_key()
dut.uecc_sign()
dut.uecc_verify()
