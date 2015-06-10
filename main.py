"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import flask
from flask import Flask
from flask_wtf import Form
from wtforms import Field
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import URL
from wtforms.validators import Optional
from wtforms.widgets import TextInput
from google.appengine.api import users

import models
from util import login


app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

APP_NAME = 'frown_destroyer'


def get_unseen_post_and_mark_as_seen():
    posts = models.Post.query().filter(models.Post.is_seen == False).fetch(limit=1)
    if not posts:
        return None
    post = posts[0]
    post.is_seen = True
    post.put()
    return post


@app.route('/')
def home():
    """Return a friendly HTTP greeting."""
    unseen_post = get_unseen_post_and_mark_as_seen()
    return flask.render_template(
        'home.html',
        title=APP_NAME,
        post=unseen_post,
    )

class PostForm(Form):
    link = StringField('Link', [DataRequired(), URL()])
    comments = TextAreaField('Comments', [Optional()])


@app.route('/admin')
@login.login_required
@login.admin_required
def admin():
    post_form = PostForm()
    posts = models.Post.query().order(models.Post.time_created).fetch()
    return flask.render_template(
        'admin.html',
        title=admin,
        form=post_form,
        posts=posts,
    )

@app.route('/admin/post', methods=('POST',))
@login.login_required
@login.admin_required
def admin_post():
    form = PostForm()
    if not form.validate_on_submit():
        print form.errors
    else:
        post = models.Post(
            link=form.link.data,
            comments=form.comments.data,
            is_seen=False,
        )
        post.put()

    return flask.redirect(flask.url_for('admin'))


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
