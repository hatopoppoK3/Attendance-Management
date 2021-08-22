import functools
import secrets

from flask import (Blueprint, g, redirect, render_template, request, session,
                   url_for)
from werkzeug.security import check_password_hash

from datastore.datastore import get_entity

login = Blueprint('login', __name__, url_prefix='/')


@login.before_app_request
def load_logged_in_user():
    session_id = session.get('session_id')

    if session_id is None:
        g.login_flag = False
    else:
        g.login_flag = True


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.login_flag:
            return view(**kwargs)

        return redirect(url_for('login.show_login'))

    return wrapped_view


@login.route('/', methods=['GET'])
def show_login():
    if g.login_flag:
        return redirect(url_for('home.show_home'))
    return render_template('login.html',
                           title='Login', login_flag=g.login_flag)


@login.route('/', methods=['POST'])
def post_login():
    username = request.form['username']
    password = request.form['password']

    user = get_entity('user', username)
    if (user is None) or not(check_password_hash(user['password'], password)):
        return redirect(url_for('login.show_login'))
    else:
        session['session_id'] = secrets.token_bytes(256)
        return redirect(url_for('home.show_home'))
