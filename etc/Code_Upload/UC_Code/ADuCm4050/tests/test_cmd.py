import serial
from time import sleep
port = '/dev/ttyACM0'

ser = serial.Serial(port, baudrate=115200)

print("Wrote {} bytes\n".format(ser.write([0x00, 0x04, 0x10, 0x44])))
#  x = [0x00, 0x04, 0x78, 0x06]

#  for i in x:
    #  ser.write(i)
    #  sleep(0.3)

ser.close()

