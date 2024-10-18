from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    protein_intake = db.Column(db.Integer) 
    calorie_intake = db.Column(db.Integer)  
    high_carb_days = db.Column(db.Integer) 
    normal_carb_days = db.Column(db.Integer)
    low_carb_days = db.Column(db.Integer)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    data = db.relationship('Data')