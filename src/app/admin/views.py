from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from .. import db
from ..models import User, Material, PriceList
from ..user.forms import ChangeStatusForm
from ..user.forms.updatePriceList import UpdatePriceListForm

admin = Blueprint('admin', __name__)


@admin.route('/users')
@login_required
def users_page():
    user_request = User.query.all()
    return render_template("admin/users.jinja2", title=f"Přehled uživatelů",
                           user_request=user_request)


@admin.route('/updatePrice/<int:id>', methods=['GET', 'POST'])
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


@admin.route('/changeStatus/<int:id>', methods=['GET', 'POST'])
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
