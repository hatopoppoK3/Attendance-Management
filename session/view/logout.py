from flask import Blueprint, flash, redirect, request, session, url_for

from models.user import User
from utility.logging import output_logging, setup_logger
from utility.session import auth_session, login_required

logout = Blueprint('logout', __name__, url_prefix='/logout')
logout_logger = setup_logger(__name__)


@logout.route('/', methods=['POST'])
@login_required
def post_logout():
    user = User(session['username'])
    if (auth_session(request.form['sessionID'])) and (user.logout_session()):
        session.clear()

        output_logging(logout_logger, 'info', f'{user.username} Logout now!')
        flash('ログアウト', category='info')
        return redirect(url_for('session.login.show_login'))

    output_logging(logout_logger, 'warning', f'Login failed {user.username}')
    flash('ログアウトエラー', category='warning')
    return redirect(url_for('home.show_home'))
