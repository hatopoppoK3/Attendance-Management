from datetime import timedelta

from flask import Flask

from account.account import account_app
from view.home import home


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.register_blueprint(account_app)
app.register_blueprint(home)
app.permanent_session_lifetime = timedelta(minutes=10)


if __name__ == '__main__':
    app.run()
