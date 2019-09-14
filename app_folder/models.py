from datetime import datetime
from app_folder import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique = True)
    email = db.Column(db.String(120), index=True, unique = True)
    password_hash = db.Column(db.String(128))
    products = db.relationship('Product', backref = 'owner', lazy = 'dynamic')

    def __repr__ (self):
        return '<User {}>'.format(self.username)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Product {}>'.format(self.name)