from flask import Blueprint, flash, redirect, request, session, url_for

from models.user import User
from utility.session import auth_session, login_required

logout = Blueprint('logout', __name__, url_prefix='/logout')


@logout.route('/', methods=['POST'])
@login_required
def post_logout():
    user = User(session['username'])
    if (auth_session(request.form['sessionID'])) and (user.delete_session()):
        session.clear()

        flash('ログアウト', category='info')
        return redirect(url_for('session.login.show_login'))

    flash('ログアウトエラー', category='alert')
    return redirect(url_for('home.show_home'))
