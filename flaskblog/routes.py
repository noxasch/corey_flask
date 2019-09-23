import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, login_manager
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, DeletePostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# posts = [
#     {
#         'author': 'Corey Schafer',
#         'title': 'Blog Post 1',
#         'content': 'First blog post content',
#         'date_posted': 'April 20, 2019'
#     },
#     {
#         'author': 'John Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second blog post content',
#         'date_posted': 'April 21, 2019'
#     }
# ]


# by default router only accept GET
@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts) # **kwargs


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'ui positive message')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # get return none if key not exist, dictionary key will raise error
            return redirect(next_page) if next_page else redirect(url_for('home')) # python ternary operator
        flash('Unsuccessful login, please check email and password', 'ui negative message')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def delete_picture(old_picture):
    os.remove(os.path.join(app.root_path, 'static/profile_pics', old_picture))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f'{random_hex}{f_ext}'
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # image resizing using PIL
    output_size = (150,150) 
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: 
            if current_user.image_file and 'default.jpeg' not in current_user.image_file:
                delete_picture(current_user.image_file)
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info has been updated', 'ui positive message')
        return redirect('account')
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{ current_user.image_file }')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','ui positive message')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)


@app.route('/post/<int:post_id>')
def post(post_id):
    form = DeletePostForm()
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, form=form)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','ui positive message')
        return redirect(url_for('post', post_id=post.id))
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','ui warning message')
    return redirect(url_for('home'))

