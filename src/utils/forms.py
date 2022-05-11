from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, SubmitField
from wtforms.validators import DataRequired
from utils.models import choices


class ValidateDate(FlaskForm):
    period = SelectField("Moneda de Destino", choices=choices)
    submit = SubmitField("Submit")

class ValidateFile(FlaskForm):
    file = FileField("Retrain file", validators=[DataRequired(message="Debes subir un archivo .csv")])
    submit = SubmitField("Submit")

class SubmitRetrain(FlaskForm):
    submit = SubmitField("Submit")