import secrets

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from werkzeug.security import generate_password_hash

from datastore.datastore import get_entity, update_entity

register = Blueprint('register', __name__, url_prefix='/register')


@register.route('/', methods=['GET'])
def show_register():
    return render_template('register.html', title='Register')


@register.route('/', methods=['POST'])
def post_register():
    username = request.form['username']
    password = request.form['password']
    password_conform = request.form['passwordConform']
    if password != password_conform:
        return redirect(url_for('register.show_register'))
    elif not(get_entity('user', username) is None):
        return redirect(url_for('register.show_register'))
    else:
        update_entity('user', username, {
                      'password': generate_password_hash(password)})
        session['session_id'] = secrets.token_bytes(256)
        return redirect(url_for('home.show_home'))
