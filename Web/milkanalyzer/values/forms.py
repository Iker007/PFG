from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ValueForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    proportion = StringField('Proporción', validators=[DataRequired()])
    description = TextAreaField('Información', validators=[DataRequired()])
    submit = SubmitField('Confirmar')

