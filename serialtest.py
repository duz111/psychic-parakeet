import serial
import ping3

def check_comstatus(port):
    try:
        ser = serial.Serial(port)
        print("{} is open".format(ser.port))
        ser.close()
    except serial.SerialException: #如果找不到或无法配置设备
        print("{} is cloesd".format(port))

def test_ping(ip_address):
    result = ping3.ping(ip_address)
    if result != None:
        print(f"成功从 {ip_address} 收到响应，延迟为 {result} 毫秒")
    else:
        print(f"无法从 {ip_address} 收到响应")

if __name__ == "__main__":#被调用时不执行此句
    port = 'COM1'
    check_comstatus(port)
    ip_address = "192.0.0.1"
    test_ping(ip_address)
