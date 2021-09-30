from flask import Blueprint

from session.view.login import login
from session.view.logout import logout
from session.view.register import register
from session.view.unregister import unregister

session = Blueprint('session', __name__)
session.register_blueprint(login)
session.register_blueprint(logout)
session.register_blueprint(register)
session.register_blueprint(unregister)
