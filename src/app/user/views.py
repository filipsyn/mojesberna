from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from sqlalchemy import desc

from . import get_user_attributes
from .forms import ChangePasswordform, ChangePersonalForm, ChangeAddressForm
from .. import db
from ..decorators import permission_required
from ..models import User, Permission, Purchase, UserStatus, Status, Address, PriceList, Material


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


@user.route('/change/personal-info', methods=['GET', 'POST'])
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


@user.route('/change/address/primary', methods=['GET', 'POST'])
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


@user.route('/change/address/secondary', methods=['GET', 'POST'])
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
    price_list = db.session.execute(''' WITH recent_prices AS (SELECT p.price_id, p.material_id
                       FROM price_list p
                                JOIN (SELECT material_id, MAX(date) AS max_date
                                      FROM price_list
                                      GROUP BY material_id) m ON p.material_id = m.material_id AND p.date = m.max_date)
    SELECT price, name
    FROM recent_prices
         JOIN price_list ON recent_prices.price_id = price_list.price_id
         JOIN materials ON recent_prices.material_id = materials.material_id;''').fetchall()

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

    total = this_months_money()

    data = dict(user_attributes=user_attributes, registration_requests=registration_requests, price_list=price_list,
                purchases=purchases, total=total)
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

@user.route('/most_redeemed', methods=['GET'])
def most_redeemed_material():
        request = db.session.execute('''
        SELECT materials.name, max(count(materials.material_id))
        FROM materials 
        JOIN purchases ON (materials.material_id=purchases.material_id) 
        JOIN users ON (users.user_id=selling_customer_id)
        WHERE users.user_id = ? GROUP BY materials.name;
         ''', current_user.user_id).fetchall()


@user.route('/months_money', methods=['GET'])
def this_months_money():
    return db.session.execute('''
                SELECT sum(price_list.price) AS price
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                JOIN purchases ON (materials.material_id=purchases.material_id)  
                JOIN users ON (users.user_id=purchases.selling_customer_id)
                WHERE users.user_id = 1;
                 ''').fetchone()





@user.route('/lives_money', methods=['GET'])
def live_earnings():
    return db.session.execute('''
                SELECT sum(price)
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                OIN purchases ON (materials.material_id=purchases.material_id)  
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? 
                 ''', current_user.user_id).fetchall()

@user.route('/total_material', methods=['GET'])
def total_bought_material(mat_name: str):
    return db.session.execute('''
                SELECT materials.name, sum(purchases.weight)
                FROM materials 
                JOIN purchases ON (materials.material_id=purchases.material_id) 
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? AND materials.name = ? 
                 ''', [current_user.user_id, mat_name]).fetchall()

@user.route('/total', methods=['GET'])
def total_bought():
    return db.session.execute('''
                    SELECT sum(purchases.weight)
                    FROM materials 
                    JOIN purchases ON (materials.material_id=purchases.material_id) 
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE users.user_id = ? AND materials.name = ?
                     ''', current_user.user_id).fetchall()

@staticmethod
def most_redeemed_material_for_all_users():
    return db.session.execute('''
            SELECT materials.name, max(count(materials.material_id))
            FROM materials 
            JOIN purchases ON (materials.material_id=purchases.material_id) 
            JOIN users ON (users.user_id=selling_customer_id)
             ''').fetchall()

@staticmethod
def this_months_money_for_all_users():
    return db.session.execute('''
                    SELECT sum(price)
                    FROM price_list 
                    JOIN materials ON (materials.material_id=price_list.material_id)
                    OIN purchases ON (materials.material_id=purchases.material_id)  
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE purchases.date = GETDATE() 
                     ''').fetchall()

@staticmethod
def live_earnings_for_all_users():
    return db.session.execute('''
                    SELECT sum(price)
                    FROM price_list 
                    JOIN materials ON (materials.material_id=price_list.material_id)
                    OIN purchases ON (materials.material_id=purchases.material_id)  
                    JOIN users ON (users.user_id=selling_customer_id)
                     ''').fetchall()

@staticmethod
def total_bought_material_for_all_users(mat_name: str):
    return db.session.execute('''
                    SELECT materials.name, sum(purchases.weight)
                    FROM materials 
                    JOIN purchases ON (materials.material_id=purchases.material_id) 
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE materials.name = ? 
                     ''', mat_name).fetchall()

@staticmethod
def total_bought_for_all_users_for_all_users():
    return db.session.execute('''
                        SELECT sum(purchases.weight)
                        FROM materials 
                        JOIN purchases ON (materials.material_id=purchases.material_id) 
                        JOIN users ON (users.user_id=selling_customer_id)
                        WHERE materials.name = ?
                         ''').fetchall()