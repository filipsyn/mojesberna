from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField


class ChangeStatusForm(FlaskForm):
    status_id = RadioField('Status', choices=[('1', 'čekající'), ('2', 'aktivní'), ('3', 'ban')])

    submit = SubmitField('Změnit')
