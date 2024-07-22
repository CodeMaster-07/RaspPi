import sqlite3
from datetime import datetime, timedelta
import random
import os

DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'battery_status.db')

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS battery_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            IP TEXT,
            MAC TEXT,
            UsbPortLocation TEXT,
            State INTEGER,
            SOC INTEGER,
            TotalVoltage REAL,
            Voltage1 REAL,
            Voltage2 REAL,
            Voltage3 REAL,
            Voltage4 REAL,
            Voltage5 REAL,
            Voltage6 REAL,
            Voltage7 REAL,
            Temperature REAL,
            UploadTime TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generate_random_data(num_records):
    data = []
    for _ in range(num_records):
        ip = "192.168.1.1"
        mac = "00-00-00-00-00-00"
        usb_port = str(random.randint(1, 10))
        state = random.randint(1, 3)
        soc = random.randint(0, 100)
        total_voltage = round(random.uniform(20.0, 24.0), 3)
        voltages = [round(random.uniform(3.0, 4.2), 3) for _ in range(7)]
        temperature = round(random.uniform(20.0, 40.0), 1)
        upload_time = (datetime.now() - timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d %H:%M:%S")
        
        data.append((
            ip, mac, usb_port, state, soc, total_voltage,
            voltages[0], voltages[1], voltages[2], voltages[3],
            voltages[4], voltages[5], voltages[6], temperature, upload_time
        ))
    return data

def insert_random_data(num_records):
    data = generate_random_data(num_records)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO battery_status (
            IP, MAC, UsbPortLocation, State, SOC, TotalVoltage,
            Voltage1, Voltage2, Voltage3, Voltage4, Voltage5,
            Voltage6, Voltage7, Temperature, UploadTime
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    insert_random_data(100)
    print("Inserted 100 random records into the database.")
