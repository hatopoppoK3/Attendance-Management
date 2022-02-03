from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from models.user import User
from session.view.login import login_required

unregister = Blueprint('unregister', __name__, url_prefix='/unregister')


@unregister.route('/', methods=['GET'])
@login_required
def show_unregister():
    return render_template('account/unregister.html', title='Unregister')


@unregister.route('/', methods=['POST'])
@login_required
def post_unregister():
    user = User(g.user['username'], g.user['userdata'])
    if user.delete_user(request.form['password']):
        session.clear()
        flash('アカウント削除完了', category='success')
        return redirect(url_for('session.login.show_login'))

    flash('アカウント削除エラー', category='alert')
    return redirect(url_for('session.unregister.show_unregister'))
