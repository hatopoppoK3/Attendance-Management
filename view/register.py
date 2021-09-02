import secrets

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for, flash)
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
    password_confirm = request.form['passwordConfirm']
    if password != password_confirm:
        flash('Password is incorrect!', category='alert')
        return redirect(url_for('register.show_register'))
    elif not(get_entity('user', username) is None):
        flash('This user already exist!', category='alert')
        return redirect(url_for('register.show_register'))
    else:
        update_entity('user', username, {
                      'password': generate_password_hash(password)})
        session['session_id'] = secrets.token_bytes(256)
        flash('Create new user and Login!', category='info')
        return redirect(url_for('home.show_home'))
