from flask import render_template, flash, redirect, url_for
from app_folder import app
from app_folder.forms import Login_form, Add_product_form, Register_form
from flask_login import current_user, login_user, logout_user, login_required
from app_folder.models import User
from flask import request
from werkzeug.urls import url_parse

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

@app.route('/product', methods=['GET', 'POST'])
def add_product():
    form = Add_product_form()
    if form.validate_on_submit():
        flash('New product {} added'.format(
            form.productname))
        return redirect(url_for('index'))
    #print(form.errors)
    return render_template('add_product.html', form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = Register_form()
    if form.validate_on_submit():
        flash('New user {} registered, id_location = {}, remember_me = {}'.format(
            form.username.data,
            form.location.data,
            form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('register_form.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
