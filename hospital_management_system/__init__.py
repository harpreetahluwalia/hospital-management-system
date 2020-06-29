from flask import  Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

from hospital_management_system import routes

