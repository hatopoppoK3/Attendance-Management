from datetime import timedelta

from flask import Flask

from config import SECRET_KEY, SESSION_LIFETIME
from session.session import session
from view.home import home

app = Flask(__name__)
app.register_blueprint(session)
app.register_blueprint(home)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(seconds=SESSION_LIFETIME)


if __name__ == '__main__':
    app.run()
