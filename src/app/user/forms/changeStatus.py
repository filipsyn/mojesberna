from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class ChangeStatusForm(FlaskForm):
    status_id = RadioField('Status', choices=[('1', 'čekající'),('2', 'aktivní'), ('3', 'ban')])

    submit = SubmitField('Změnit')
