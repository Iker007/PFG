from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from milkanalyzer.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 4, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):

        user = User.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError('Username already taken. Choose a different one')

    def validate_email(self, email):

        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('Email already registered. Have you forgotten your password?')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 4, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    profile_picture = FileField('Change profile picture', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Change information')

    def validate_username(self, username):

        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()

            if user:
                raise ValidationError('Username already taken. Choose a different one')

    def validate_email(self, email):

        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError('Email already registered. Try another one')

class ResetPassRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset password')

    def validate_email(self, email):

        user = User.query.filter_by(email = email.data).first()

        if user is None:
            raise ValidationError('There is no account with that email. You have to register first.')

class ResetPassForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')