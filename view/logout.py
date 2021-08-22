from flask import Blueprint, redirect, session, url_for

logout = Blueprint('logout', __name__, url_prefix='/logout')


@logout.route('/', methods=['POST'])
def post_logout():
    session.clear()

    return redirect(url_for('login.show_login'))
