import serial
import mysql.connector
from datetime import datetime
import time
import socket
import uuid

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

def get_mac_address():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    return mac_address

def read_battery_data(serial_port):
    try:
        ser = serial.Serial(serial_port, 9600, timeout=1)
        ser.write(b'\x01\x05\x31\x30\x00\x04\x04')
        data = ser.read(26)  # Read 26 bytes
        ser.close()
        if len(data) < 26:
            raise ValueError("Incomplete data received")
        return data
    except serial.SerialException:
        raise ValueError(f"Cannot open serial port {serial_port}")
    except Exception as e:
        raise ValueError(f"Error reading from {serial_port}: {e}")

def parse_battery_data(data):
    state = data[4]
    soc = data[5]
    total_voltage = (data[7] << 8 | data[6]) * 0.001  # 전체 전압은 0.001V 단위
    voltages = [(data[9 + i * 2] << 8 | data[8 + i * 2]) * 0.001 for i in range(7)]
    temperature = (data[23] << 8 | data[22]) * 0.1  # 온도는 0.1도 단위
    bcc = data[24]
    eot = data[25]

    return {
        'State': state,
        'SOC': soc,
        'TotalVoltage': total_voltage,
        'Voltages': voltages,
        'Temperature': temperature,
        'BCC': bcc,
        'EOT': eot,
        'RawData': data
    }

def send_data_to_mysql(data, raspberry_pi, usb_port, ip_address, mac_address, rack_number):
    try:
        connection = mysql.connector.connect(
            host='your_mysql_server_ip',
            user='your_mysql_user',
            password='your_mysql_password',
            database='your_database_name'
        )

        cursor = connection.cursor()

        call_proc_query = """
        CALL InsertBatteryInfoProc(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        insert_query = """
        INSERT INTO transfer_battery_info 
        (battery_status, battery_level, battery_voltage, cell_voltage1, cell_voltage2, cell_voltage3, cell_voltage4, cell_voltage5, cell_voltage6, cell_voltage7, usb_port_number, client_ip, mac, rack_number, cell_temperature)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            data['State'],
            data['SOC'],
            data['TotalVoltage'],
            f'{data["Voltages"][0]:.3f}V',
            f'{data["Voltages"][1]:.3f}V',
            f'{data["Voltages"][2]:.3f}V',
            f'{data["Voltages"][3]:.3f}V',
            f'{data["Voltages"][4]:.3f}V',
            f'{data["Voltages"][5]:.3f}V',
            f'{data["Voltages"][6]:.3f}V',
            usb_port,
            ip_address,
            mac_address,
            rack_number,
            data['Temperature']
        ))

        connection.commit()
        cursor.close()
        connection.close()
        print(f'Data successfully uploaded to MySQL for {raspberry_pi} {usb_port}')
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def print_battery_data(data, raspberry_pi, usb_port):
    raw_data_hex = ' '.join([f'{byte:02X}' for byte in data['RawData']])
    state_str = "방전" if data['State'] == 2 else "충전"
    voltages_str = "\n".join([f'전압 {i+1}: {v:.3f}V ({v*1000:.0f}mV)' for i, v in enumerate(data['Voltages'])])
    output = f"""
        Raspberry Pi: {raspberry_pi}, USB Port: {usb_port}
        Raw Data: {raw_data_hex}
        SOH: {data['RawData'][0]:02X}
        Size: {data['RawData'][1]:02X}
        Seq: {data['RawData'][2]:02X}
        Command: {data['RawData'][3]:02X}
        State: {data['State']} ({state_str})
        SOC: {data['SOC']}% (배터리 충전율)
        전체 전압: {data['TotalVoltage']:.1f}V
        {voltages_str}
        온도: {data['Temperature']:.1f}도
        BCC: 0x{data['BCC']:02X}
        EOT: 0x{data['EOT']:02X}
     """
    print(output)

if __name__ == '__main__':
    raspberry_pi = 'PI1'
    ip_address = get_ip_address()
    mac_address = get_mac_address()
    rack_number = 1 

    while True:
        for usb_port in range(1, 11):
            serial_port = f'/dev/usb_hub_port{usb_port}'
            try:
                data = read_battery_data(serial_port)
                if data:
                    parsed_data = parse_battery_data(data)
                    print_battery_data(parsed_data, raspberry_pi, f'USB{usb_port}')
                    send_data_to_mysql(parsed_data, raspberry_pi, f'USB{usb_port}', ip_address, mac_address, rack_number)
                else:
                    print(f'No data from {serial_port}')
            except Exception as e:
                print(f'USB {usb_port}: 정보없음 - {e}')
        time.sleep(5)
