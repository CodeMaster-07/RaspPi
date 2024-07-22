from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta
import random

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

def insert_random_data(count):
    with app.app_context():
        db.session.query(BatteryStatus).delete()  # Clear existing data
        db.session.commit()

        for _ in range(count):
            battery = BatteryStatus(
                raspberry_pi=f"PI{random.randint(1, 10)}",
                usb_port=f"USB{random.randint(1, 10)}",
                state=random.randint(1, 3),
                soc=random.randint(0, 100),
                total_voltage=random.uniform(20.0, 25.0),
                voltage_1=random.uniform(3.0, 3.5),
                voltage_2=random.uniform(3.0, 3.5),
                voltage_3=random.uniform(3.0, 3.5),
                voltage_4=random.uniform(3.0, 3.5),
                voltage_5=random.uniform(3.0, 3.5),
                voltage_6=random.uniform(3.0, 3.5),
                voltage_7=random.uniform(3.0, 3.5),
                temperature=random.uniform(20.0, 30.0),
                upload_time=datetime.now() - timedelta(minutes=random.randint(0, 1000))
            )
            db.session.add(battery)
        
        db.session.commit()

def fetch_all_data():
    with app.app_context():
        return BatteryStatus.query.order_by(BatteryStatus.upload_time.desc()).all()

if __name__ == "__main__":
    insert_random_data(100)
    print("Inserted random data.")
