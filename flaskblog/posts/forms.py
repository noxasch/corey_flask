from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, SubmitField


class PostForm(FlaskForm):
    title = StringField('Title', [validators.InputRequired()])
    content = TextAreaField('Content', [validators.InputRequired()])
    submit = SubmitField('Post')


class DeletePostForm(FlaskForm):
    pass
