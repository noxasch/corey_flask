from datetime import datetime
from flask_login import UserMixin
from flaskblog import db, login_manager


@login_manager.user_loader # this is how the login manager retrieve the current user
def load_user(user_id):
    return User.query.get(int(user_id))

# currently intellisense for ORM not working on vscode
# flask-pylint just ignore the error as well as flake8
# not a linting issue https://github.com/PyCQA/pylint/issues/1973
# same on pycharm
# create DB table model
# the class is User (Capitalized) but by default the table name is gonna be in all lowercase
class User(db.Model, UserMixin):
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
        