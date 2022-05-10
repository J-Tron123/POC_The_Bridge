from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, regexp
from utils.models import choices


class ValidateDate(FlaskForm):
    period = SelectField("Moneda de Destino",  choices=choices)
    submit = SubmitField("Submit")

class ValidateFile(FlaskForm):
    file = FileField("Retrain file", validators=[DataRequired(message="You must upload a .csv file"), regexp("^\[^/\\]\.csv$")])
    submit = SubmitField("Submit")