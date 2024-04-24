def calculate_CRC(hex_string):
    class FramerRTU():
        @classmethod
        def generate_crc16_table(cls) -> list[int]:
            #生产CRC查找表
            result = []
            for byte in range(256):
                crc = 0x0000
                for _ in range(8):
                    if (byte ^ crc) & 0x0001:
                        crc = (crc >> 1) ^ 0xA001
                    else:
                        crc >>= 1
                    byte >>= 1
                result.append(crc)
            return result
        crc16_table: list[int] = [0]

        @classmethod
        def check_CRC(cls, data: bytes, check: int) -> bool:
            return cls.compute_CRC(data) == check

        @classmethod
        def compute_CRC(cls, data: bytes) -> int:
            """
            modbus 的 CRC 值从 0xffff 开始
            """
            crc = 0xFFFF
            for data_byte in data:
                idx = cls.crc16_table[(crc ^ int(data_byte)) & 0xFF]
                crc = ((crc >> 8) & 0xFF) ^ idx
            swapped = ((crc << 8) & 0xFF00) | ((crc >> 8) & 0x00FF)
            return swapped

    FramerRTU.crc16_table = FramerRTU.generate_crc16_table()
    hex_data = bytes.fromhex(hex_string)#十六进制字符串转换为字节串
    crc_value = FramerRTU.compute_CRC(hex_data)
    return print(hex(crc_value))


calculate_CRC('01033B000002')

# hex_string = '01033B000002'#0xc92f 
# ser1 = serial.Serial('COM1') 
# ser2 = serial.Serial('COM2')
# ser1.write(b'01033B000002')
# data = ser2.read(12)
# data2=data.decode("ascii")
# print(data2)


# hex_data = bytes.fromhex(data2)
# crc_value = FramerRTU.compute_CRC(hex_data)
# hex_value = hex(crc_value)
# print(hex_value)   

# # 关闭串口
# ser1.close()
# ser2.close()
