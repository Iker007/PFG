from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from milkanalyzer.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recúerdame')
    submit = SubmitField('Iniciar sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min = 4, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Dirección', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):

        user = User.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError('Usuario ya en uso. Elige uno diferente')

    def validate_email(self, email):

        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('Email ya en uso. ¿Has olvidado tu contraseña?')

class UpdateProfileForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min = 4, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Dirección', validators=[DataRequired()])
    profile_picture = FileField('Modificar imagen de perfil', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Modificar información')

    def validate_username(self, username):

        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()

            if user:
                raise ValidationError('Usuario ya en uso. Elige uno diferente')

    def validate_email(self, email):

        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError('Email ya en uso. Prueba uno diferente')

class ResetPassRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Cambiar contraseña')

    def validate_email(self, email):

        user = User.query.filter_by(email = email.data).first()

        if user is None:
            raise ValidationError('No existe una cuenta con ese email. Tienes que registrarte primero.')

class ResetPassForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cambiar contraseña')