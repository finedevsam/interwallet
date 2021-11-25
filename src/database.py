from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_merchant = db.Column(db.Boolean(), default=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    merchants=db.relationship('Merchant', backref="user")
    
    
    def __repr__(self) -> str:
        return 'User >>> {self.username}'
   


class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_code = db.Column(db.Text(), nullable=True)
    merchant_name = db.Column(db.Text(), nullable=True)
    merchant_address = db.Column(db.Text(), nullable=True)
    contact_phone = db.Column(db.Text(), nullable=True)
    business_email = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now()) 
    apikey=db.relationship('APIKey', backref="merchant")  
       
     
    def get_image(self):
        if self.image:
                return "http://127.0.0.1:5000/static/uploads/" + self.image
        return ''
    

class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    secret_key = db.Column(db.Text(), nullable=True)
    public_key = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.secret_key)