from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class ChangeRoleForm(FlaskForm):
    role_id = RadioField('Role', choices=[('1', 'uživatel'), ('2', 'pracovník'), ('3', 'admin')])

    submit = SubmitField('Změnit')
