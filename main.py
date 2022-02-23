from flask import Flask, render_template
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from session.session import session
from view.home import home

app = Flask(__name__)
app.register_blueprint(session)
app.register_blueprint(home)
app.config.from_pyfile('config.py')


@app.errorhandler(Exception)
def show_error(error):
    if not(isinstance(error, NotFound) or isinstance(error, BadRequest)):
        error = InternalServerError
        error.name = error.__name__
    return render_template('error.html',
                           title=error.name, statusCode=error.code)


if __name__ == '__main__':
    app.run()
