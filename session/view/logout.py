from flask import Blueprint, flash, g, redirect, session, url_for

from models.user import User
from session.view.login import login_required

logout = Blueprint('logout', __name__, url_prefix='/logout')


@logout.route('/', methods=['POST'])
@login_required
def post_logout():
    user = User(g.user['username'], g.user['userdata'])
    if user.delete_session():
        session.clear()

        flash('ログアウト', category='info')
        return redirect(url_for('session.login.show_login'))

    flash('ログアウトエラー', category='alert')
    return redirect(url_for('home.show_home'))
