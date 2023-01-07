from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from . import get_user_attributes
from .forms import ChangePasswordform, ChangeStatusForm
from .forms.updatePriceList import UpdatePriceListForm
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


@user.route('/dashboard')
@login_required
def dashboard_page():
    user_attributes = get_user_attributes(current_user)
    price_list = Material.query.join(PriceList, Material.material_id == PriceList.material_id).add_columns(
        Material.material_id, PriceList.price_id, Material.name, PriceList.price).all()
    registration_request = User.query.filter_by(status_id=1).all()
    return render_template("user/dashboard.jinja2", title=f"Přehled uživatele {current_user.login}",
                           user_attributes=user_attributes, price_list=price_list,
                           registration_request=registration_request)


@user.route('/updatePrice/<int:id>', methods=['GET', 'POST'])
@login_required
def update_price(id):
    form = UpdatePriceListForm()
    price_to_update = PriceList.query.get_or_404(id)
    if request.method == "POST":
        price_to_update.price = request.form['price']
        try:
            db.session.commit()
            flash('Změna hesla proběhla úspěšně')
            return render_template("user/updatePriceList.jinja2", form=form, price_to_update=price_to_update)
        except:
            flash('Error')
            return render_template("user/updatePriceList.jinja2", form=form, price_to_update=price_to_update)
    else:
        return render_template("user/updatePriceList.jinja2", form=form, price_to_update=price_to_update)
@user.route('/changeStatus/<int:id>', methods=['GET', 'POST'])
@login_required
def change_status(id):
    form = ChangeStatusForm()
    status_to_change = User.query.get_or_404(id)
    if request.method == "POST":
        status_to_change.status_id = request.form['status_id']
        try:
            db.session.commit()
            flash('Změna statusu proběhla úspěšně')
            return render_template("user/changeStatus.jinja2", form=form, status_to_change=status_to_change)
        except:
            flash('Error')
            return render_template("user/changeStatus.jinja2", form=form, status_to_change=status_to_change)
    else:
        return render_template("user/changeStatus.jinja2", form=form, status_to_change=status_to_change)