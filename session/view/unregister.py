from datastore.datastore import delete_entity, get_entity
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash

from session.view.login import login_required


unregister = Blueprint('unregister', __name__, url_prefix='/unregister')


@unregister.route('/', methods=['GET'])
@login_required
def show_unregister():
    return render_template('account/unregister.html', title='Unregister')


@unregister.route('/', methods=['POST'])
@login_required
def post_unregister():
    if request.form['sessionID'] != session['session_id']:
        session.clear()
        flash('Session Error! Force Logout!', 'alert')
        return redirect(url_for('session.login.show_login'))

    username = request.form['username']
    password = request.form['password']

    user = get_entity('user', username)
    if user is None:
        flash('Unregister Failed!', category='alert')
        return redirect(url_for('session.unregister.show_unregister'))

    elif not(check_password_hash(user['password'], password)):
        flash('Password is incorrect!', category='alert')
        return redirect(url_for('session.unregister.show_unregister'))

    delete_entity('user', username)
    session.clear()
    flash('Unregister Success!', category='success')
    return redirect(url_for('session.login.show_login'))
