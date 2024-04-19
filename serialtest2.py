import serial
ser2 = serial.Serial('COM2')
ser1 = serial.Serial('COM1')  
print(ser1.name)
print(ser2.name)         
ser1.write(b'01033B000002')     
try:
    # 读取数据
    data = ser2.read(12)  # 读取10个字节的数据
    print("Received data:", data)
    print("Received data:", data.decode('ascii'))
except Exception as e:
    print("Error:", e)
finally:
    # 关闭串口
    ser1.close()
    ser2.close()
