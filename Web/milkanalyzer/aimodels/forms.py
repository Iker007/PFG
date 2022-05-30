from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class AIModelForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    type = StringField('Tipo', validators=[DataRequired()])
    description = TextAreaField('Información', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired()])
    submit = SubmitField('Confirmar')


class SelectFileForm(FlaskForm):
    file_name = StringField('Nombre del archivo generado', validators=[DataRequired()])
    csv_file = FileField('Adjuntar csv delimitado por ;', validators=[DataRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Confirmar')

