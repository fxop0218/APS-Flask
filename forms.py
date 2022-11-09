from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PersonForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname")
    email = StringField("Email", validators=[DataRequired()])
    send = SubmitField("Send")
