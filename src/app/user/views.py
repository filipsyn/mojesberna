from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from .forms import ChangePasswordform
from .. import db
from ..models import User

user = Blueprint('user', __name__)


@user.route('/changePassword', methods=['GET', 'POST'])

def view_change_password_page():
    form = ChangePasswordform()
    if form.validate_on_submit():
        current_user.password = form.password.data

        db.session.commit()
        flash('Změna hesla proběhla úspěšně')
        return redirect(url_for('auth.logout'))
    return render_template('user/changePassword.jinja2', title='zmena', form=form)
