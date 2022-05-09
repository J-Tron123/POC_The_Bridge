from flask_wtf import FlaskForm
from wtforms import DateField, FileField, SubmitField
from wtforms.validators import DataRequired, regexp


class ValidateDate(FlaskForm):
    date = DateField("Date", validators=[DataRequired(message="You must enter a Date")])
    submit = SubmitField("Submit")

class ValidateFile(FlaskForm):
    file = FileField("Retrain file", validators=[DataRequired(message="You must upload a .csv file"), regexp("^\[^/\\]\.csv$")])
    submit = SubmitField("Submit")