from datetime import timedelta

from flask import Flask

from session.session import session
from view.home import home


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.register_blueprint(session)
app.register_blueprint(home)
app.permanent_session_lifetime = timedelta(minutes=15)


if __name__ == '__main__':
    app.run()
