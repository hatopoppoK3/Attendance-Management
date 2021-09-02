from datetime import timedelta

from flask import Flask

from view.home import home
from view.login import login
from view.logout import logout
from view.register import register
from view.unregister import unregister

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(unregister)
app.permanent_session_lifetime = timedelta(minutes=10)

if __name__ == '__main__':
    app.run()
