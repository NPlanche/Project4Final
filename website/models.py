#Database models
#importing the db from __init__ 
from . import db
#helps login users
from flask_login import UserMixin
from sqlalchemy.sql import func

#Defining Database Object Schema
#Notes 
class Note(db.Model):
    #id
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #relationship one to many => one user has many notes
    #referencing the tables name in sql User-->user the .id is the property
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#USER
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #here your are referencing name of class 
    notes = db.relationship('Note')