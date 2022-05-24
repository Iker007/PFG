from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class AIModelForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    type = StringField('Tipo', validators=[DataRequired()])
    description = TextAreaField('Información', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired()])
    submit = SubmitField('Confirmar')

