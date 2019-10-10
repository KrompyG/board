import os
import uuid
from flask import render_template, flash, redirect, url_for, request
from app_folder import app
from app_folder.forms import (Login_form, Add_product_form, Register_form,
                              Search_form)
from flask_login import current_user, login_user, logout_user, login_required
from app_folder.models import User, Product
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app_folder import db
from config import form_photo_path

# checking file's extension
def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS'])

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if authenticated user tries to login again
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        # wrong user's data
        if ((user is None) or not (user.check_password(form.password.data))):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        # if everething is good
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # if next_page does't exist or next_page has absolute path (unsecure)
        if ((not next_page) or (url_parse(next_page).netloc != '')):
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form = form)

#TODO make another version of photo path
@app.route('/product', methods=['GET', 'POST'])
def add_product():
    form = Add_product_form()
    if form.validate_on_submit():
        product = Product(name = form.productname.data,
                          category_id = form.category.data,
                          user_id = current_user.id)

        photo = form.photo.data
        # creating folders if needed
        if photo and allowed_file(photo.filename):
            # forming new unique name for product photo
            extension = photo.filename.rsplit('.', 1)[1]
            photo_uid_name = str(uuid.uuid4().hex) + '.' + extension
            photo.save(os.path.join(app.config['PRODUCT_PHOTO_FOLDER'], photo_uid_name))
            product.photo_name = photo_uid_name

        db.session.add(product)
        db.session.commit()
        flash('Новый продукт {} успешно добавлен!'.format(
            form.productname.data))
        return redirect(url_for('index'))
    #print(form.errors)
    return render_template('add_product.html', form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    # if authenticated user tries to registrate again
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Register_form()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data,
                    location_id = form.location.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('register_form.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/my_offers', methods=['GET', 'POST'])
@login_required
def my_offers():
    products = Product.query.filter_by(owner = current_user).order_by(Product.category_id.asc())
    return render_template('my_offers.html', products = products, get_path = form_photo_path)

@app.route('/search', methods=['GET','POST'])
def search_product():
    form = Search_form()
    if form.validate_on_submit():        
        products = Product.query.join(Product.owner).filter(
            (Product.category != None) if (form.category.data == 0) else (Product.category_id == form.category.data),
            (User.location_id != None) if (form.location.data == 0) else (User.location_id == form.location.data),
            (Product.name != None) if (form.productname.data == '') else (Product.name == form.productname.data)
        )
        return render_template('search_form.html', products = products.all(),
                                form = form, get_path = form_photo_path)
    products = Product.query.all()
    return render_template('search_form.html', products = products,
                            form = form, get_path = form_photo_path)

@app.route('/product/<product_id>')
def show_product(product_id):
    product = Product.query.filter_by(id = product_id).first()
    return render_template('product_page.html', product = product,
                            get_path = form_photo_path)

#TODO make another version of photo path
@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    # for editing product Add_product_form could be used
    form = Add_product_form()
    product = Product.query.filter_by(id = product_id).first()
    if product.owner == current_user:
        if form.validate_on_submit():
            product.name = form.productname.data
            product.category_id = form.category.data
            new_photo = form.photo.data
            # validatig photo
            if new_photo and allowed_file(new_photo.filename):
                extension = new_photo.filename.rsplit('.', 1)[1]
                new_photo_uid_name = str(uuid.uuid4().hex) + '.' + extension
                new_photo.save(os.path.join(app.config['PRODUCT_PHOTO_FOLDER'], new_photo_uid_name))
                # checking that product has path_to_photo
                if product.photo_name is not None:
                    old_photo_path = os.path.join(app.config['PRODUCT_PHOTO_FOLDER'], product.photo_name)
                    # deleting old photo
                    if (os.path.exists(old_photo_path)):
                        os.remove(old_photo_path)
                # writing path to the new photo
                product.photo_name = new_photo_uid_name
        
            db.session.commit()
            flash('Изменения информации о продукте {} сохранены!'.format(
                  form.productname.data))
            return redirect(url_for('show_product', product_id = product_id))
        elif request.method == 'GET':
            form.productname.data = product.name
            form.category.data = product.category_id
        return render_template('edit_product.html', form = form, product = product,
                                get_path = form_photo_path)
    return redirect(url_for('show_product', product_id = product_id))
