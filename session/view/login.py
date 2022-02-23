from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from models.user import User
from utility.session import auth_session, create_session

login = Blueprint('login', __name__, url_prefix='/')


@login.before_app_request
def load_logged_in_user():
    if session.get('username'):
        g.session = True
    else:
        g.session = False


@login.route('/', methods=['GET'])
@create_session
def show_login():
    if g.session:
        return redirect(url_for('home.show_home'))
    return render_template('session/login.html', title='Login')


@login.route('/', methods=['POST'])
def post_login():
    user = User(request.form['username'])
    if (auth_session(request.form['sessionID'])) and \
            (user.create_session(request.form['password'])):
        session['username'] = user.username
        flash('ログイン', category='info')
        return redirect(url_for('home.show_home'))

    session.clear()
    flash('ログイン失敗', category='alert')
    return redirect(url_for('session.login.show_login'))
