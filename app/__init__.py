from flask import Flask, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from app.db import db
from app.models import User, Book


# Implying "Factory" pattern
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        return ('<h1>It works</h1>'
               f'<p><i>Users on site:</i> {User.query.count()}</p>'
               f'<p><i>Books on site:</i> {Book.query.count()}</p>')

    return app


if __name__ == '__main__':
    app.run()
