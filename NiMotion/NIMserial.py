import serial
from calculate_CRC import calculate_CRC
import time

def SendCommand(command):
    bytes_data = bytes.fromhex(command)#转成16进制
    print(bytes_data)
    ser.write(bytes_data)
    time.sleep(0.01)  # 延时 0.01 秒

ser = serial.Serial('COM3', 115200)
commands = [
    '01 10 03 C2 00 01 02 00 01 44 72',
    '01 10 03 E7 00 02 04 00 00 4E 20 9C 89',#设目标位置2w
    # '01 10 03 E7 00 02 04 00 00 27 10 B2 CD',#设目标位置1w
    '01 10 03 F8 00 02 04 00 00 27 10 F3 81',
    '01 10 03 FC 00 02 04 00 00 9C 40 80 BE',
    '01 10 03 FE 00 02 04 00 00 9C 40 01 67',
    '01 10 03 80 00 01 02 00 06 0A 92',
    '01 10 03 80 00 01 02 00 07 CB 52',
    '01 10 03 80 00 01 02 00 0F CA 94',
    '01 10 03 80 00 01 02 00 1F CB 58'
]

for command in commands:
    SendCommand(command)

ser.close()  # 关闭串口
