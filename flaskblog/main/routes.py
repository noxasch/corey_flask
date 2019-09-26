from flask import Blueprint, render_template, request
from flaskblog.models import Post

main = Blueprint('main', __name__)


# by default router only accept GET
@main.route('/')
@main.route('/home')
def home():
    # posts = Post.query.order_by(Post.date_posted.desc()).all()
    # change to use pagination
    # read from GET params, set type to int
    # if value is not int, it will throw an error
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', posts=posts) # **kwargs


@main.route('/about')
def about():
    return render_template('about.html', title='About')