from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    print("Database initialized and tables created.")
