from flask import render_template, flash, redirect, url_for
from app_folder import app
from app_folder.forms import Login_form, Add_product_form

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Maxim'}
    return render_template('index.html', user = user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form = form)

@app.route('/product', methods=['GET', 'POST'])
def add_product():
    form = Add_product_form()
    if form.validate_on_submit():
        flash('New product {} added'.format(
            form.productname))
        return redirect(url_for('index'))
    print(form.errors)
    return render_template('add_product.html', form = form)