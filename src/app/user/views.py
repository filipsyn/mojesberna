from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import get_user_attributes
from .forms import ChangePasswordform, ChangePersonalForm, ChangeAddressForm
from .. import db
from ..decorators import permission_required
from ..models import User, Material, PriceList, Permission, Purchase, UserStatus, Status, Address

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


@user.route('/changePersonal', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SELF_MANAGEMENT)
def view_change_personal_page():
    form = ChangePersonalForm()

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.telephone_number = form.telephone_number.data

        db.session.commit()

        flash('Změna údajů proběhla úspěšně')
        return redirect(url_for('user.view_dashboard_page'))

    return render_template('user/changePersonal.jinja2', title='zmena', form=form)


@user.route('/changeAddress', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SELF_MANAGEMENT)
def view_change_address_page():
    form = ChangeAddressForm()
    if form.validate_on_submit():
        address = Address(
            form.street.data,
            form.house_number.data,
            form.city.data,
            form.zip_code.data
        )
        current_user.permanent_residence = address
        db.session.add(address)
        db.session.commit()

        flash('Změna údajů proběhla úspěšně')
        return redirect(url_for('user.view_dashboard_page'))
    return render_template('user/changeAddress.jinja2', title='zmena', form=form)


@user.route('/changeSecondaryAddress', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SELF_MANAGEMENT)
def view_change_secondary_address_page():
    form = ChangeAddressForm()
    if form.validate_on_submit():
        address = Address(
            form.street.data,
            form.house_number.data,
            form.city.data,
            form.zip_code.data
        )
        current_user.temporary_residence = address
        db.session.add(address)
        db.session.commit()

        flash('Změna údajů proběhla úspěšně')
        return redirect(url_for('user.view_dashboard_page'))
    return render_template('user/changeSecondAddress.jinja2', title='zmena', form=form)


@user.route('/dashboard')
@login_required
@permission_required(Permission.ACCESS)
def view_dashboard_page():
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

    if current_user.is_administrator() or current_user.is_worker():
        purchases = Purchase.query. \
            filter_by(buying_employee_id=current_user.user_id) \
            .order_by(Purchase.purchase_id) \
            .limit(5) \
            .all()
    else:
        purchases = Purchase.query. \
            filter_by(selling_customer_id=current_user.user_id) \
            .order_by(Purchase.purchase_id) \
            .limit(5) \
            .all()

    data = dict(user_attributes=user_attributes, registration_requests=registration_requests, price_list=price_list,
                purchases=purchases)
    return render_template("user/dashboard.jinja2", title=f"Přehled uživatele {current_user.login}", data=data)


@user.route('/<id>/confirm')
@login_required
@permission_required(Permission.USER_ADMINISTRATION)
def confirm_user(id):
    searched_user = User.query.get_or_404(id)
    if searched_user.status.name == UserStatus.WAITING.value:
        searched_user.confirm()
        db.session.commit()
        flash(f"Registrace uživatele {searched_user.login} potvrzena", 'success')
    return redirect(url_for('admin.view_users_page'))


@user.route('<id>/ban')
@login_required
@permission_required(Permission.USER_ADMINISTRATION)
def ban_user(id):
    searched_user = User.query.get_or_404(id)
    if searched_user.status.name == UserStatus.ACTIVE.value:
        searched_user.ban()
        db.session.commit()
        flash(f"Uživatel {searched_user.login} byl zablokován", 'warning')
    return redirect(url_for('admin.view_users_page'))


@user.route('<id>/unban')
@login_required
@permission_required(Permission.USER_ADMINISTRATION)
def unban_user(id):
    searched_user = User.query.get_or_404(id)
    if searched_user.status.name == UserStatus.BANNED.value:
        searched_user.unban()
        db.session.commit()
        flash(f"Uživatel {searched_user.login} byl odblokován", 'warning')
    return redirect(url_for('admin.view_users_page'))
