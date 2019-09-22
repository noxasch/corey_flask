from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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
@app.route('/home')
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