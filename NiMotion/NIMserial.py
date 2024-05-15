import serial
from calculate_CRC import FramerRTU
import time

class Scissors():
    def __init__(self):
        self.ser = serial.Serial('COM3', 115200)#设置com口
        self.FramerRTU = FramerRTU()
        self.commands = [
        '01 10 03 C2 00 01 02 00 01', #设置为轮廓位置模式
        '01 10 03 F8 00 02 04 00 00 27 10', #设置目标速度 6081h（03F8h） 10000
        '01 10 03 FC 00 02 04 00 00 9C 40', #设置加速度 6083h（03FCh）为 40000
        '01 10 03 FE 00 02 04 00 00 9C 40', #设置减速度 6083h（03FEh）为 40000
        '01 10 03 80 00 01 02 00 06', #设置 6040h（0380h）为 0x6，使电机准备
        '01 10 03 80 00 01 02 00 07', #设置 6040h（0380h）为 0x7，使电机失能
        '01 10 03 80 00 01 02 00 0F', #设置 6040h（0380h）为 0xF，使电机使能
        ]

    def SendCommand(self, command):
        FramerRTU.crc16_table = FramerRTU.generate_crc16_table()
        hex_data = bytes.fromhex(command)#十六进制字符串转换为字节串
        crc_value = self.FramerRTU.compute_CRC(hex_data)#计算CRC
        bytes_data = crc_value.to_bytes(2, byteorder='big')#整数转字节串
        hex_string = hex_data + bytes_data
        self.ser.write(hex_string)
        print(hex_string)
        time.sleep(0.01)  # 延时 0.01 秒
        
    def InitialCommands(self):
        for command in self.commands:
            self.SendCommand(command)

    def BackOrigin():
    #TODO 原点回归模式
        pass 

    def OpenScissors(self):
        self.InitialCommands()
        self.SendCommand('01 10 03 E7 00 02 04 00 00 ff ff')#设置目标位置
        self.SendCommand('01 10 03 80 00 01 02 00 1F')#使电机运动
    
    def CloseScissors(self):
        self.InitialCommands()
        self.SendCommand('01 10 03 E7 00 02 04 00 00 00 00')#设置目标位置
        self.SendCommand('01 10 03 80 00 01 02 00 1F')#使电机运动
    
    def __del__(self):
        self.ser.close()  # 确保被销毁时关闭串口

scissors = Scissors()
scissors.CloseScissors()


