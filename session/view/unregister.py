from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from models.user import User
from utility.session import auth_session, create_session, login_required

unregister = Blueprint('unregister', __name__, url_prefix='/unregister')


@unregister.route('/', methods=['GET'])
@login_required
@create_session
def show_unregister():
    return render_template('session/unregister.html', title='Unregister')


@unregister.route('/', methods=['POST'])
@login_required
def post_unregister():
    user = User(session['username'])
    if (auth_session(request.form['sessionID'])) and \
            (user.delete_user(request.form['password'])):
        session.clear()
        flash('アカウント削除完了', category='success')
        return redirect(url_for('session.login.show_login'))

    flash('アカウント削除エラー', category='alert')
    return redirect(url_for('session.unregister.show_unregister'))
