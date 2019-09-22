from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, validators, SubmitField, BooleanField

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=2, max=20)])
    email = StringField('Email',[validators.DataRequired(),validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [
        validators.DataRequired(),
         validators.EqualTo('password', message='Password do not match')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',[validators.DataRequired(),validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
