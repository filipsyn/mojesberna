from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import get_user_attributes
from .forms import ChangePasswordform
from .. import db
from ..decorators import permission_required
from ..models import User, Material, PriceList, Permission, Purchase, UserStatus, Status

user = Blueprint('user', __name__)


@user.route('/changePassword', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SELF_MANAGEMENT)
def view_change_password_page():
    form = ChangePasswordform()
    if form.validate_on_submit():
        current_user.password = form.password.data

        db.session.commit()
        flash('Změna hesla proběhla úspěšně')
        return redirect(url_for('auth.logout'))
    return render_template('user/changePassword.jinja2', title='zmena', form=form)


@user.route('/dashboard')
@login_required
@permission_required(Permission.ACCESS)
def dashboard_page():
    user_attributes = get_user_attributes(current_user)
    price_list = Material.query. \
        join(PriceList, Material.material_id == PriceList.material_id) \
        .add_columns(Material.material_id, PriceList.price_id, Material.name, PriceList.price) \
        .all()

    waiting_status = Status.query.filter_by(name=UserStatus.WAITING.value).first()

    registration_requests = User.query \
        .filter_by(status_id=waiting_status.status_id) \
        .order_by(User.user_id) \
        .limit(5) \
        .all()

    price_list = {
        'Noviny': 2.70,
        'Železo': 4.50,
        'Měď': 85,
        'Mosaz': 45,
        'Olovo': 20
    }

    return render_template("user/dashboard.jinja2", title=f"Přehled uživatele {current_user.login}",
                           user_attributes=user_attributes, price_list=price_list,
                           registration_request=registration_request)
