from flask import app
from sqlalchemy.sql.functions import user
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    full_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(150))
    NRIC = db.Column(db.String(150))
    date_pick = db.Column(db.String(150))
    gender = db.Column(db.String(150))
    SymptomsResult = db.Column(db.Integer)
    cancelReason = db.relationship('Cancel')


class Employer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login_email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    employer_id = db.Column(db.String(150))


class Cancel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(150))
    remarks = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


