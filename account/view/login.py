import functools
import secrets

from datastore.datastore import get_entity
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash

login = Blueprint('login', __name__, url_prefix='/')


@login.before_app_request
def load_logged_in_user():
    g.session_id = session.get('session_id')
    g.username = session.get('username')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.session_id:
            return view(**kwargs)

        return redirect(url_for('account_app.login.show_login'))

    return wrapped_view


@login.route('/', methods=['GET'])
def show_login():
    if g.session_id:
        return redirect(url_for('home.show_home'))
    return render_template('account/login.html', title='Login')


@login.route('/', methods=['POST'])
def post_login():
    username = request.form['username']
    password = request.form['password']

    user = get_entity('user', username)
    if (user is None) or not(check_password_hash(user['password'], password)):
        flash('Login Failed!', category='alert')
        return redirect(url_for('account_app.login.show_login'))

    session['session_id'] = secrets.token_hex(64)
    session['username'] = username
    flash('Now Login!', category='info')
    return redirect(url_for('home.show_home'))
