from hospital_management_system import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    
    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    # def get_password(self, password):
    #     return check_password_hash(self.password, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)