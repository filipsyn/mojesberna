from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from sqlalchemy import desc

from . import get_user_attributes
from .forms import ChangePasswordform, ChangePersonalForm, ChangeAddressForm
from .. import db
from ..blueprints.stats.services.statistics import Statistics
from ..decorators import permission_required
from ..models import User, Permission, Purchase, UserStatus, Status, Address

user = Blueprint('user', __name__)


@user.route('/change/password', methods=['GET', 'POST'])
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


@user.route('<id>/settings', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SELF_MANAGEMENT)
def view_change_personal_page(id):
    # Page is only accessible by workers and user it belongs to
    if not ((current_user.user_id == int(id)) or current_user.is_administrator() or current_user.is_worker()):
        abort(403)

    edited_user = User.query.get_or_404(id)

    form = ChangePersonalForm()

    if form.validate_on_submit():
        edited_user.first_name = form.first_name.data
        edited_user.last_name = form.last_name.data
        edited_user.telephone_number = form.telephone_number.data

        db.session.commit()

        flash('Změna údajů proběhla úspěšně')
        return redirect(url_for('user.view_dashboard_page'))

    return render_template('user/changePersonal.jinja2', title='zmena', form=form, user=edited_user)


@user.route('<id>/change/address/primary', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SELF_MANAGEMENT)
def view_change_address_page(id):
    # Page is only accessible by workers and user it belongs to
    if not ((current_user.user_id == int(id)) or current_user.is_administrator() or current_user.is_worker()):
        abort(403)

    edited_user = User.query.get_or_404(id)

    form = ChangeAddressForm()
    if form.validate_on_submit():
        address = Address(
            form.street.data,
            form.house_number.data,
            form.city.data,
            form.zip_code.data
        )
        edited_user.permanent_residence = address
        db.session.add(address)
        db.session.commit()

        flash('Změna údajů proběhla úspěšně')
        return redirect(url_for('user.view_dashboard_page'))
    return render_template('user/changeAddress.jinja2', title='Změna adresy', form=form)


@user.route('<id>/change/address/secondary', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SELF_MANAGEMENT)
def view_change_secondary_address_page(id):
    # Page is only accessible by workers and user it belongs to
    if not ((current_user.user_id == int(id)) or current_user.is_administrator() or current_user.is_worker()):
        abort(403)

    edited_user = User.query.get_or_404(id)

    form = ChangeAddressForm()
    if form.validate_on_submit():
        address = Address(
            form.street.data,
            form.house_number.data,
            form.city.data,
            form.zip_code.data
        )
        edited_user.temporary_residence = address
        db.session.add(address)
        db.session.commit()

        flash('Změna údajů proběhla úspěšně')
        return redirect(url_for('user.view_dashboard_page'))
    return render_template('user/changeSecondAddress.jinja2', title='Změna sekundární adresy', form=form)


@user.route('/dashboard')
@login_required
@permission_required(Permission.ACCESS)
def view_dashboard_page():
    user_attributes = get_user_attributes(current_user)
    price_list = Statistics.get_price_list()

    waiting_status = Status.query.filter_by(name=UserStatus.WAITING.value).first()

    registration_requests = User.query \
        .filter_by(status_id=waiting_status.status_id) \
        .order_by(User.user_id) \
        .limit(5) \
        .all()

    if current_user.is_administrator() or current_user.is_worker():
        purchases = Purchase.query. \
            filter_by(buying_employee_id=current_user.user_id) \
            .order_by(desc(Purchase.date)) \
            .limit(5) \
            .all()
    else:
        purchases = Purchase.query. \
            filter_by(selling_customer_id=current_user.user_id) \
            .order_by(desc(Purchase.date)) \
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


@user.route('<id>')
@login_required
def view_profile_page(id: int):
    # Page is only accessible by workers and user it belongs to
    if not ((current_user.user_id == int(id)) or current_user.is_administrator() or current_user.is_worker()):
        abort(403)

    found_user = User.query.get_or_404(id)

    if found_user.is_administrator() or found_user.is_worker():
        purchases = Purchase.query. \
            filter_by(buying_employee_id=found_user.user_id) \
            .order_by(Purchase.purchase_id) \
            .limit(5) \
            .all()
    else:
        purchases = Purchase.query. \
            filter_by(selling_customer_id=found_user.user_id) \
            .order_by(Purchase.purchase_id) \
            .limit(5) \
            .all()

    stats = []

    data = dict(user=found_user, purchases=purchases, stats=stats)
    return render_template('user/profile.jinja2', data=data,
                           title=f"Profil {found_user.first_name} {found_user.last_name}")
