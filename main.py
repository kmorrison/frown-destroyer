"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import flask
from flask import Flask
from google.appengine.api import users

from util import login


app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

APP_NAME = 'frown_destroyer'


@app.route('/')
def home():
    """Return a friendly HTTP greeting."""
    return flask.render_template(
        'home.html',
        title=APP_NAME,
    )


@app.route('/me')
@login.login_required
def me():
    return flask.render_template(
        'me.html',
        title=APP_NAME,
        user=users.get_current_user(),
    )

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

app.secret_key = 'Change me.'
