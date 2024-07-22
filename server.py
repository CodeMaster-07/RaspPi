from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(os.path.dirname(__file__), 'battery_status.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BatteryStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raspberry_pi = db.Column(db.String(10))
    usb_port = db.Column(db.String(10))
    state = db.Column(db.Integer)
    soc = db.Column(db.Integer)
    total_voltage = db.Column(db.Float)
    voltage_1 = db.Column(db.Float)
    voltage_2 = db.Column(db.Float)
    voltage_3 = db.Column(db.Float)
    voltage_4 = db.Column(db.Float)
    voltage_5 = db.Column(db.Float)
    voltage_6 = db.Column(db.Float)
    voltage_7 = db.Column(db.Float)
    temperature = db.Column(db.Float)
    upload_time = db.Column(db.DateTime)

@app.route('/api/upload', methods=['POST'])
def upload_battery_status():
    data = request.get_json()
    battery_status = BatteryStatus(
        raspberry_pi=data.get('RaspberryPi'),
        usb_port=data.get('UsbPort'),
        state=data.get('State'),
        soc=data.get('SOC'),
        total_voltage=data.get('TotalVoltage'),
        voltage_1=data.get('Voltage1'),
        voltage_2=data.get('Voltage2'),
        voltage_3=data.get('Voltage3'),
        voltage_4=data.get('Voltage4'),
        voltage_5=data.get('Voltage5'),
        voltage_6=data.get('Voltage6'),
        voltage_7=data.get('Voltage7'),
        temperature=data.get('Temperature'),
        upload_time=datetime.strptime(data.get('UploadTime'), '%Y-%m-%d %H:%M:%S')
    )
    db.session.add(battery_status)
    db.session.commit()
    return jsonify({'result': 'success', 'resultCode': 100, 'resultDesc': 'Data uploaded successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080)
