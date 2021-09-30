from flask import Blueprint, flash, redirect, session, url_for

from session.view.login import login_required

logout = Blueprint('logout', __name__, url_prefix='/logout')


@logout.route('/', methods=['POST'])
@login_required
def post_logout():
    session.clear()

    flash('Now Logout!', category='info')
    return redirect(url_for('session.login.show_login'))
