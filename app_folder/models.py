import os
import uuid
from app_folder import app
from datetime import datetime
from app_folder import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app_folder import login
from app_folder.utilits import allowed_file


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))
    vk_id = db.Column(db.Integer, unique = True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref = 'inhabitants')
    products = db.relationship('Product', backref = 'owner', lazy = 'dynamic')
    messages = db.relationship('Message', backref = 'author')
    dialogs = db.relationship('Dialog')

    def __repr__ (self):
        return '<User {} {} {}>'.format(self.first_name, self.last_name, self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    photo_name = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
    dialogs = db.relationship('Dialog')

    def __repr__(self):
        return '<Product {}>'.format(self.name)

    # deleting current product photo
    def delete_photo(self):
        if self.photo_name is not None:
            photo_path = os.path.join(app.config['PRODUCT_PHOTO_FOLDER'], self.photo_name)
            # deleting photo
            if (os.path.exists(photo_path)):
                os.remove(photo_path)
            self.photo_name = ''
        return

    # adding new product photo
    def add_photo(self, photo):
        if photo and allowed_file(photo.filename):
            # forming new unique name for product photo
            extension = photo.filename.rsplit('.', 1)[1]
            photo_uid_name = str(uuid.uuid4().hex) + '.' + extension
            photo.save(os.path.join(app.config['PRODUCT_PHOTO_FOLDER'], photo_uid_name))
            self.photo_name = photo_uid_name
            return True
        else:
            return False

    # replacing current product photo with new one
    def replace_photo(self, photo):
        if photo and allowed_file(photo.filename):
            # forming new unique name for product photo
            extension = photo.filename.rsplit('.', 1)[1]
            photo_uid_name = str(uuid.uuid4().hex) + '.' + extension
            photo.save(os.path.join(app.config['PRODUCT_PHOTO_FOLDER'], photo_uid_name))
            self.delete_photo()
            self.photo_name = photo_uid_name
            return True
        else:
            return False        


# for flask_login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Location {}>'.format(self.name)


class Dialog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship('Message')

def __repr__(self):
        return '<Dialog id={}'.format(self.id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dialog_id = db.Column(db.Integer, db.ForeignKey('dialog.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Message about product_id={} from user_id={}>'.format(self.product_id,self.author_id)
