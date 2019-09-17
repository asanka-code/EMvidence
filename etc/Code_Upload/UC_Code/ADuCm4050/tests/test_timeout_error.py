import serial
from time import sleep
port = '/dev/ttyACM0'

ser = serial.Serial(port, baudrate=115200, timeout=0.5)

print("Wrote {} bytes\n".format(ser.write([0x00, 0x04, 0x09, 0x01])))
res = ser.read(8)
print("Got {} bytes\n".format(", ".join(["0x{:02X}".format(i) for i in res])))

ser.close()

