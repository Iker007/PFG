from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    description = TextAreaField('Information', validators=[DataRequired()])
    submit = SubmitField('Confirm')

