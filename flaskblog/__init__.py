import os # set email and password (Sensitive info) as environment variable
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # will handle session etc
from flask_mail import Mail
from flaskblog.config import Config


csrf = CSRFProtect()
# source: https://flask-wtf.readthedocs.io/en/stable/csrf.html

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'ui warning message'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    csrf.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    return app
