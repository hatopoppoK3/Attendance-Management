import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from models.user import User

login = Blueprint('login', __name__, url_prefix='/')


@login.before_app_request
def load_logged_in_user():
    if not(session.get('username')):
        g.session = False
        return

    user = User(session.get('username'))
    if user.auth_session(session.get('session_id')):
        g.session = True
        g.user = user.__dict__
    else:
        g.session = False


def login_required(func):
    @functools.wraps(func)
    def wrapped_view(**kwargs):
        if g.session:
            return func(**kwargs)

        return redirect(url_for('session.login.show_login'))

    return wrapped_view


@login.route('/', methods=['GET'])
def show_login():
    raise AttributeError
    if g.session:
        return redirect(url_for('home.show_home'))
    return render_template('account/login.html', title='Login')


@login.route('/', methods=['POST'])
def post_login():
    user = User(request.form['username'])
    if user.create_session(request.form['password']):
        session['username'] = user.username
        session['session_id'] = user.userdata['session_id']
        flash('ログイン', category='info')
        return redirect(url_for('home.show_home'))

    session.clear()
    flash('ログイン失敗', category='alert')
    return redirect(url_for('session.login.show_login'))
