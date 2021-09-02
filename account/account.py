from flask import Blueprint

from account.view.login import login
from account.view.logout import logout
from account.view.register import register
from account.view.unregister import unregister

account_app = Blueprint('account_app', __name__)
account_app.register_blueprint(login)
account_app.register_blueprint(logout)
account_app.register_blueprint(register)
account_app.register_blueprint(unregister)
