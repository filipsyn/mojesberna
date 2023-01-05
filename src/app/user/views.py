from flask import Blueprint, render_template, redirect, url_for, flash


from .forms import changePasswordform
from .. import db
from ..models import User

user = Blueprint('user', __name__)

@user.route('/changePassword', methods=['GET', 'POST'])
def view_changePassword_page():
    form = changePasswordform()


    return render_template('user/changePassword.jinja2', title='zmena', form=form)
