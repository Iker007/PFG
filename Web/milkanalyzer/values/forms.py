from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ValueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    proportion = StringField('Proportion', validators=[DataRequired()])
    description = TextAreaField('Information', validators=[DataRequired()])
    submit = SubmitField('Confirm')

