from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import get_user_attributes
from .forms import ChangePasswordform
from .. import db
from ..models import User, Material, PriceList

user = Blueprint('user', __name__)


@user.route('/changePassword', methods=['GET', 'POST'])
@login_required
def view_change_password_page():
    form = ChangePasswordform()
    if form.validate_on_submit():
        current_user.password = form.password.data

        db.session.commit()
        flash('Změna hesla proběhla úspěšně')
        return redirect(url_for('auth.logout'))
    return render_template('user/changePassword.jinja2', title='zmena', form=form)


@user.route("/dashboard")
@login_required
def dashboard_page():
    user_attributes = get_user_attributes(current_user)
    price_list = Material.query.join(PriceList, Material.material_id == PriceList.material_id).add_columns(Material.material_id, Material.name, PriceList.price).all()
    return render_template("user/dashboard.jinja2", title=f"Přehled uživatele {current_user.login}",
                           user_attributes=user_attributes, price_list=price_list)
