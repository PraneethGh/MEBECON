from proj import db
from datetime import datetime
#from flask_gtts import gtts
from PyDictionary import PyDictionary 

class Clinic(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    dept = db.Column(db.String(30),unique=True,nullable=False)
    name=db.Column(db.String(120),unique=True,nullable=False)
    contact=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(100),nullable=False)
    hours=db.Column(db.String(20),nullable=False)
    rating=db.Column(db.Numeric,nullable=False)

    def __repr__(self):
        return f'{self.dept} : {self.name} : {self.hours}'