import os # set email and password (Sensitive info) as environment variable
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # will handle session etc
from flask_mail import Mail
from flaskblog.config import config

app = Flask(__name__)
csrf = CSRFProtect(app)
# source: https://flask-wtf.readthedocs.io/en/stable/csrf.html
# app.debug = True

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# can be created using python secrets > secrtets.token_hex(BITS)
app.secret_key = config['SECRET_KEY']

# SQLAlchemy config
# relative path using /// from current file
# sqlite db will be created in current folder
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = config['MAIL_SERVER']
app.config['MAIL_PORT'] = config['MAIL_PORT']
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = config['USER_EMAIL']
app.config['MAIL_PASSWORD'] = config['PASSWORD']

# Why set to False
# https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
# https://github.com/honmaple/flask-msearch/issues/23
# https://github.com/pallets/flask-sqlalchemy/issues/365

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'ui warning message'

mail = Mail(app)

from flaskblog import routes # avoid circular import
