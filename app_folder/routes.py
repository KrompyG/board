import os, requests
from flask import render_template, flash, redirect, url_for, request
from app_folder import app
from app_folder.forms import (Login_form, Register_form,
                              Add_offer_form, Add_request_form,
                              Edit_product_form, Search_form, 
                              Edit_profile_form, Send_message_form,
                              Delete_product_form, Create_dialog_form)
from flask_login import current_user, login_user, logout_user, login_required
from app_folder.models import User, Product, Message, Dialog
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app_folder import db
from app_folder.utilits import form_photo_path
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_


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
    url = 'http://oauth.vk.com/authorize?client_id={}&client_secret={}&v=5.102&response_type=code&redirect_uri={}&scope=email'.format(
                app.config['APP_ID'],
                app.config['PROTECTED_KEY'],
                'http://localhost:5000/vk_login' #temporarily can't use url_for()
             )
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
    return render_template('login.html', form = form, vk_url = url)


@app.route('/add_offer', methods=['GET', 'POST'])
def add_offer():
    form = Add_offer_form()
    if form.validate_on_submit():
        product = Product(name = form.productname.data,
                          category_id = form.category.data,
                          user_id = current_user.id,
                          status = app.config['OFFER_STATUS'])
        product.add_photo(form.photo.data)

        db.session.add(product)
        db.session.commit()
        flash('Новое предложение {} успешно добавлено!'.format(
            form.productname.data))
        return redirect(url_for('index'))
    return render_template('add_offer.html', form = form)


@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    form = Add_request_form()
    if form.validate_on_submit():
        product = Product(name = form.productname.data,
                          category_id = form.category.data,
                          user_id = current_user.id,
                          status = app.config['REQUEST_STATUS'])

        db.session.add(product)
        db.session.commit()
        flash('Новый запрос {} успешно добавлен!'.format(
            form.productname.data))
        return redirect(url_for('index'))
    return render_template('add_request.html', form = form)


@app.route('/register', methods=['GET','POST'])
def register():
    # if authenticated user tries to registrate again
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Register_form()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                    first_name = form.first_name.data, last_name = form.last_name.data,
                    email = form.email.data, location_id = form.location.data)
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


@app.route('/offers', methods=['GET','POST'])
def search_offers():
    form = Search_form()
    if form.validate_on_submit():        
        products = Product.query.join(Product.owner).filter(
            (Product.category != None) if (form.category.data == 0)
                else (Product.category_id == form.category.data),

            (User.location_id != None) if (form.location.data == 0)
                else (User.location_id == form.location.data),
                
            (Product.name != None) if (form.productname.data == '')
                else (Product.name == form.productname.data),

            Product.status == app.config['OFFER_STATUS'] #product offer
        )
        return render_template('search_offers.html', products = products.all(),
                                form = form, get_path = form_photo_path)
    products = Product.query.filter_by(
        status = app.config['OFFER_STATUS']
    ).all()
    return render_template('search_offers.html', products = products,
                            form = form, get_path = form_photo_path)


@app.route('/my_offers', methods=['GET', 'POST'])
@login_required
def my_offers():
    form = Delete_product_form()
    products = Product.query.filter_by(
        owner = current_user,
        status = app.config['OFFER_STATUS']
    ).order_by(Product.category_id).all()
    return render_template('my_offers.html', products = products,
            get_path = form_photo_path, form = form)


@app.route('/requests', methods=['GET','POST'])
def search_requests():
    form = Search_form()
    if form.validate_on_submit():        
        products = Product.query.join(Product.owner).filter(
            (Product.category != None) if (form.category.data == 0)
                else (Product.category_id == form.category.data),

            (User.location_id != None) if (form.location.data == 0)
                else (User.location_id == form.location.data),
                
            (Product.name != None) if (form.productname.data == '')
                else (Product.name == form.productname.data),

            Product.status == app.config['REQUEST_STATUS'] #product request
        )
        return render_template('search_requests.html', products = products.all(),
                                form = form, get_path = form_photo_path)
    products = Product.query.filter_by(
        status = app.config['REQUEST_STATUS']
    ).all()
    return render_template('search_requests.html', products = products,
                            form = form, get_path = form_photo_path)


@app.route('/my_requests', methods=['GET', 'POST'])
@login_required
def my_requests():
    products = Product.query.filter_by(
        owner = current_user,
        status = app.config['REQUEST_STATUS']
    ).order_by(Product.category_id.asc())
    return render_template('my_requests.html', products = products)


@app.route('/product/<product_id>')
def show_product(product_id):
    product = Product.query.filter_by(id = product_id).first()
    if current_user != product.owner:
        dialog = Dialog.query.filter_by(
            product_id = product.id,
            customer_id = current_user.id
        ).all() #this query will return only one dialog
        create_dialog_form = Create_dialog_form()
        return render_template('product_page.html', product = product,
                        get_path = form_photo_path, dialog_list = dialog,
                        create_dialog_form = create_dialog_form)
    else: #current_user is product owner
        delete_product_form = Delete_product_form()
        if product.status == app.config['OFFER_STATUS']:
            delete_product_form.next_page.data = url_for('my_offers')
        elif product.status == app.config['REQUEST_STATUS']:
            delete_product_form.next_page.data = url_for('my_requests')
        dialogs = Dialog.query.filter_by(
            product_id = product.id
        ).all()
        return render_template('product_page.html', product = product,
                    get_path = form_photo_path, dialog_list = dialogs,
                    create_dialog = create_dialog, delete_product_form = delete_product_form)


#TODO make another version of photo path
@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    form = Edit_product_form()
    product = Product.query.filter_by(id = product_id).first()
    if product.owner == current_user:
        if form.validate_on_submit():
            product.name = form.productname.data
            product.category_id = form.category.data
            if product.get_has_photo():
                product.replace_photo(form.photo.data)
        
            db.session.commit()
            flash('Изменения информации о продукте {} сохранены!'.format(
                  form.productname.data))
            return redirect(url_for('show_product', product_id = product_id))
        elif request.method == 'GET':
            form.productname.data = product.name
            form.category.data = product.category_id
        return render_template('edit_product.html', form = form, product = product,
                                get_path = form_photo_path, has_photo = product.get_has_photo())
    return redirect(url_for('show_product', product_id = product_id))


@app.route('/vk_login', methods=['GET', 'POST'])
def vk_login():
    code = request.args.get('code')
    if code:
        url_for_tocken = 'https://oauth.vk.com/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}'.format(
                     app.config['APP_ID'],
                     app.config['PROTECTED_KEY'],
                     'http://localhost:5000/vk_login', #temporarily can't use url_for()
                     code
                 )
        response = requests.get(url_for_tocken).json()
        token = response.get('access_token')
        user_vk_id = response.get('user_id')
        
        user = User.query.filter_by(vk_id = user_vk_id).first()
        if (user == None):
            email = response.get('email')
            url_for_info = 'https://api.vk.com/method/users.get?user_id={}&access_token={}&v=5.102'.format(user_vk_id, token)
            response_dict = requests.get(url_for_info).json().get('response')[0] # response dict with args
            first_name = response_dict.get('first_name')
            last_name = response_dict.get('last_name')

            user = User(first_name = first_name,
                        last_name = last_name,
                        email = email,
                        vk_id = user_vk_id)
            user.username = user.first_name + '_' + user.last_name + '_' + str(user.vk_id)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('edit_profile'))
                        
        else:
            login_user(user)
            return redirect(url_for('index'))
    else:
        flash('Что-то пошло не так...')
        return redirect(url_for('index'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = Edit_profile_form()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.location_id = form.location.data
        db.session.commit()
        flash('Изменения в профиле сохранены')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.location.data = current_user.location_id
    return render_template('edit_profile.html', form = form, app = app)


@app.route('/add_vk_id')
@login_required
def add_vk_id():
    if current_user.vk_id is not None:
        return redirect(url_for('index'))
    code = request.args.get('code')
    if code:
        url_for_tocken = 'https://oauth.vk.com/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}'.format(
                     app.config['APP_ID'],
                     app.config['PROTECTED_KEY'],
                     'http://localhost:5000/add_vk_id', #temporarily can't use url_for()
                     code
                 )
        response = requests.get(url_for_tocken).json()
        token = response.get('access_token')
        user_vk_id = response.get('user_id')
        try:
            current_user.vk_id = user_vk_id
            db.session.commit()
            flash('Аккаунт Вконтакте успешно добавлен')
            return redirect(url_for('index'))
        except IntegrityError as e:
            flash('Этот аккаунт VK уже используется')
            return redirect(url_for('index'))
        else:
            pass
    flash('Что-то пошло не так...')
    return redirect(url_for('index'))


@app.route('/dialog/<dialog_id>',  methods=['GET', 'POST'])
@login_required
def show_dialog(dialog_id):
    form = Send_message_form()
    current_dialog = Dialog.query.filter_by(id=dialog_id).first()
    product_owner = Product.query.filter_by(id=current_dialog.product_id).first().owner
    if form.validate_on_submit():
        new_message = Message(
            dialog_id = dialog_id,
            author_id = current_user.id,
            body = form.textarea.data
        )
        db.session.add(new_message)
        db.session.commit()
        form.textarea.data = ''
    messages = Message.query.filter_by(
        dialog_id = dialog_id
    ).order_by(Message.timestamp)
    return render_template('show_dialog.html', messages=messages, form=form)

@app.route('/create_dialog', methods=['POST'])
@login_required
def create_dialog():
    product_id = int(request.form['product_id'])
    customer_id = int(request.form['customer_id'])
    dialog = Dialog(
        product_id = product_id,
        customer_id = customer_id
    )
    db.session.add(dialog)
    db.session.commit()
    return redirect(url_for('show_dialog', dialog_id = dialog.id))



@app.route('/delete_product', methods=['POST'])
def delete_product():
    id = int(request.form['index'])
    next_page = request.form['next_page']
    product = Product.query.filter_by(id = id).first()
    if product:
        product.delete_photo()
        for dialog in product.dialogs:
            db.session.delete(dialog)
        db.session.delete(product)
        db.session.commit()
        flash('Продукт успешно удалён')
    else:
        flash('Данного продукта не существует')
    # if next_page has absolute path (unsecure)
    if (url_parse(next_page).netloc != ''):
        next_page = url_for('index')
    return redirect(next_page)
