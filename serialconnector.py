import serial
import struct

portenta_in = serial.Serial('/dev/cu.usbmodem3878348033301')
uno_out = serial.Serial('/dev/cu.usbmodem14201')

labels = [
    'angry',
    'fearful',
    'happy',
    'neutral',
    'sad',
    'surprised'
]

while True:
    datain = int(portenta_in.readline())
    uno_out.write(struct.pack('i',datain))
    print(labels[datain])