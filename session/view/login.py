from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from models.user import User
from utility.logging import output_logging, setup_logger
from utility.session import auth_session, create_session

login = Blueprint('login', __name__, url_prefix='/')
login_logger = setup_logger(__name__)


@login.route('/', methods=['GET'])
@create_session
def show_login():
    if session.get('username'):
        return redirect(url_for('attendance.home.show_home'))
    return render_template('session/login.html', title='Login')


@login.route('/', methods=['POST'])
def post_login():
    user = User(request.form['username'])
    if (auth_session(request.form['sessionID'])) and \
            (user.login_session(request.form['password'])):
        session['username'] = user.username

        output_logging(login_logger, 'info', f'{user.username} Login now!')
        flash('ログイン', category='info')
        return redirect(url_for('attendance.home.show_home'))

    session.clear()
    output_logging(login_logger, 'warning', f'Login failed {user.username}')
    flash('ログイン失敗', category='warning')
    return redirect(url_for('session.login.show_login'))
