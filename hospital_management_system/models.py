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
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.String(250), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_of_admission = db.Column(db.Date, nullable=False)
    type_of_bed = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    state = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(100), nullable=False)


class Medicines(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)


class MedicinesIssued(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    med_id = db.Column(db.Integer, nullable=False)
    p_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
