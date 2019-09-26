from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, validators, SubmitField, BooleanField, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=2, max=20)])
    email = StringField('Email', [validators.DataRequired(),validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Password do not match')
    ])
    submit = SubmitField('Sign Up')

    # custom validation
    # def validate_field(self, field):
    #     if True: raise ValidationError('Validation Message')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: raise ValidationError('Username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: raise ValidationError('Email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',[validators.DataRequired(),validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=2, max=20)])
    email = StringField('Email', [validators.DataRequired(),validators.Email()])
    picture = FileField('Update Profile Picture', [FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user: raise ValidationError('Username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user: raise ValidationError('Email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(),validators.Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user: raise ValidationError('There is no account associated with this email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', [validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Password do not match')
    ])
    submit = SubmitField('Reset Password')
