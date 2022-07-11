from flask import Blueprint

from attendance.view.home import home

attendance = Blueprint('attendance', __name__, url_prefix='/attendance')
attendance.register_blueprint(home)
