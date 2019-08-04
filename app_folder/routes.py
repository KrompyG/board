from flask import render_template
from app_folder import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Maxim'}
    return render_template('index.html', user = user)