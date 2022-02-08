from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from models.user import User

register = Blueprint('register', __name__, url_prefix='/register')


@register.route('/', methods=['GET'])
def show_register():
    if g.session:
        return redirect(url_for('home.show_home'))
    return render_template('session/register.html', title='Register')


@register.route('/', methods=['POST'])
def post_register():
    user = User(request.form['username'])
    if user.create_user(request.form['password'],
                        request.form['passwordConfirm']):
        session['username'] = user.username
        session['session_id'] = user.userdata['session_id']
        flash('アカウント作成', category='info')
        return redirect(url_for('home.show_home'))

    flash('アカウント作成失敗', category='alert')
    return redirect(url_for('session.register.show_register'))
