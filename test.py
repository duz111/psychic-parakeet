from __future__ import annotations
import serial
class FramerRTU():
    """Modbus RTU frame type.

    [ Start Wait ] [Address ][ Function Code] [ Data ][ CRC ]
      3.5 chars     1b         1b               Nb      2b

    * Note: due to the USB converter and the OS drivers, timing cannot be quaranteed
    neither when receiving nor when sending.
    """
    @classmethod
    def generate_crc16_table(cls) -> list[int]:
        """Generate a crc16 lookup table.

        .. note:: This will only be generated once
        """
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
        """Check if the data matches the passed in CRC.

        :param data: The data to create a crc16 of
        :param check: The CRC to validate
        :returns: True if matched, False otherwise
        """
        return cls.compute_CRC(data) == check

    @classmethod
    def compute_CRC(cls, data: bytes) -> int:
        """Compute a crc16 on the passed in bytes.

        The difference between modbus's crc16 and a normal crc16
        is that modbus starts the crc value out at 0xffff.

        :param data: The data to create a crc16 of
        :returns: The calculated CRC
        """
        crc = 0xFFFF
        for data_byte in data:
            idx = cls.crc16_table[(crc ^ int(data_byte)) & 0xFF]
            crc = ((crc >> 8) & 0xFF) ^ idx
        swapped = ((crc << 8) & 0xFF00) | ((crc >> 8) & 0x00FF)
        return swapped

FramerRTU.crc16_table = FramerRTU.generate_crc16_table()

# data = b'\x01\x03\x04\x5B\x80\x00\x08'
# formatted_str = ' 0x'.join(format(x, '02X') for x in data)
# formatted_str ='0x' +  formatted_str


# 字符串转换为列表
# string = "Hello,World"
# string_list = string.split(',')  # 使用逗号作为分隔符拆分字符串
# print(string_list)  # 输出: ['Hello', 'World']
# 列表转换为字符串
# my_list = ['Hello', 'World']
# my_string = ','.join(my_list)  # 使用逗号连接列表中的元素
# print(my_string)  # 输出: 'Hello,World'


# hex_string = '01033B000002'#0xc92f

# string_list=hex_string.split(',')
# print(string_list)   


# hex_data = bytes.fromhex(hex_string)
# crc_value = FramerRTU.compute_CRC(hex_data)
# hex_value = hex(crc_value)
# print(hex_value) 

ser1 = serial.Serial('COM1') 
ser2 = serial.Serial('COM2')
ser1.write(b'01033B000002')
data = ser2.read(12)
data2=data.decode("ascii")
print(data2)


hex_data = bytes.fromhex(data2)
crc_value = FramerRTU.compute_CRC(hex_data)
hex_value = hex(crc_value)
print(hex_value)   

# hex_data = bytes.fromhex(data.hex())

# # 计算 CRC，传入的参数为字节串
# crc_value = FramerRTU.compute_CRC(hex_data)

# # 将 CRC 值转换为十六进制字符串
# hex_value = hex(crc_value)

# print(hex_value)

# 关闭串口
ser1.close()
ser2.close()

# crc_value = FramerRTU.compute_CRC(data2[:-2])
# # 将 CRC 值转换为十六进制字符串
# hex_value = hex(crc_value)
# print(hex_value)