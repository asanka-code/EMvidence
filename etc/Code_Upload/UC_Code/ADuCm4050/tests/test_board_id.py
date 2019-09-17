import serial
from time import sleep
port = '/dev/ttyACM0'

ser = serial.Serial(port, baudrate=115200, timeout=None)
command = 0x501
board_id = 567
args = [(board_id & 0xFF), (board_id >> 8) & 0xFF]

length = 2 + 2 + len(args)
len0 = (length >> 8) & 0xFF
len1 = length & 0xFF

cmd0 = (command >> 8) & 0xFF
cmd1 = command & 0xFF

send_bytes = [len0, len1] + [cmd0, cmd1] + args

print("Wrote {} bytes\n".format(ser.write(send_bytes)))
print("{}\n".format(", ".join(["0x{:02X}".format(i) for i in send_bytes])))

res = ser.read(6)
print("Got {} bytes\n".format(", ".join(["0x{:02X}".format(i) for i in res])))

ser.close()

