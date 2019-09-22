from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
# source: https://flask-wtf.readthedocs.io/en/stable/csrf.html
# app.debug = True

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# can be created using python secrets > secrtets.token_hex(BITS)
app.secret_key = 'b41125056068fe63e6196ab61ec5b3259ecbdf36ebebbf54985857e82038316d'

# SQLAlchemy config
# relative path using /// from current file
# sqlite db will be created in current folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Why set to False
# https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
# https://github.com/honmaple/flask-msearch/issues/23
# https://github.com/pallets/flask-sqlalchemy/issues/365

db = SQLAlchemy(app)

from flaskblog import routes # avoid circular import
