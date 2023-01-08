from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from ...models.material import Material


class EditPriceForm(FlaskForm):
    opts = QuerySelectField(query_factory=Material.get_query, allow_blank=False, get_label=lambda x: x.name)
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Editovat Cenu')

