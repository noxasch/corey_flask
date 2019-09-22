from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
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

# currently intellisense for ORM not working on vscode
# flask-pylint just ignore the error as well as flake8
# not a linting issue https://github.com/PyCQA/pylint/issues/1973
# same on pycharm
# create DB table model
# the class is User (Capitalized) but by default the table name is gonna be in all lowercase
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100))
    image_file = db.Column(db.String(160), nullable=False, default='default.jpeg')
    # has relationship to Post model, backref add another column to post, lazy justify that we can actually easily get the post this user created
    # this is not a table but extra query
    posts = db.relationship('Post', backref='author', lazy=True) 

    # __repr__ determine how when object is printed ?
    # __scr__
    # __ is magic method
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First blog post content',
        'date_posted': 'April 20, 2019'
    },
    {
        'author': 'John Doe',
        'title': 'Blog Post 2',
        'content': 'Second blog post content',
        'date_posted': 'April 21, 2019'
    }
]

# by default router only accept GET
@app.route('/')
def home():
    return render_template('home.html', posts=posts) # **kwargs

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'ui positive message')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'ui positive message')
            return redirect(url_for('home'))
        flash('Unsuccessful login, please check username and password', 'ui negative message')
    return render_template('login.html', form=form, title='Login')


if __name__ == "__main__":
    app.run(debug=True)