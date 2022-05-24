from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class RestaurantForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    location = StringField('Ubicación', validators=[DataRequired()])
    description = TextAreaField('Information', validators=[DataRequired()])
    submit = SubmitField('Confirm')

