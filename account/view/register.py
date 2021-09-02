import secrets

from datastore.datastore import get_entity, update_entity
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import generate_password_hash

register = Blueprint('register', __name__, url_prefix='/register')


@register.route('/', methods=['GET'])
def show_register():
    return render_template('account/register.html', title='Register')


@register.route('/', methods=['POST'])
def post_register():
    username = request.form['username']
    password = request.form['password']
    password_confirm = request.form['passwordConfirm']
    if password != password_confirm:
        flash('Password is incorrect!', category='alert')
        return redirect(url_for('account_app.register.show_register'))

    elif not(get_entity('user', username) is None):
        flash('This user already exist!', category='alert')
        return redirect(url_for('account_app.register.show_register'))

    update_entity('user', username, {
        'password': generate_password_hash(password)})
    session['session_id'] = secrets.token_bytes(256)
    session['username'] = username
    flash('Create new user and Login!', category='info')
    return redirect(url_for('home.show_home'))
