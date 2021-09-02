import secrets

from flask import (Blueprint, g, redirect, render_template, request, session,
                   url_for, flash)
from werkzeug.security import check_password_hash

from datastore.datastore import get_entity, delete_entity
from view.login import login_required

unregister = Blueprint('unregister', __name__, url_prefix='/unregister')


@unregister.route('/', methods=['GET'])
@login_required
def show_unregister():
    return render_template('unregister.html',
                           title='Unregister', username=g.username)


@unregister.route('/', methods=['POST'])
@login_required
def post_unregister():
    username = request.form['username']
    password = request.form['password']

    user = get_entity('user', username)
    if user is None:
        flash('Unregister Failed!', category='alert')
        return redirect(url_for('unregister.show_unregister'))
    elif not(check_password_hash(user['password'], password)):
        flash('Password Wrong!', category='alert')
        return redirect(url_for('unregister.show_unregister'))
    else:
        delete_entity('user', username)
        session.clear()
        flash('Unregister Success!', category='info')
        return redirect(url_for('login.show_login'))
