from flask import Blueprint, flash, redirect, session, url_for

logout = Blueprint('logout', __name__, url_prefix='/logout')


@logout.route('/', methods=['POST'])
def post_logout():
    session.clear()

    flash('Now Logout!', category='info')
    return redirect(url_for('login.show_login'))
