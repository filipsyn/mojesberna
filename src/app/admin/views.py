from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required


from .forms import AddUserForm
from .. import db
from ..models import User, Material, PriceList, Status, Address
from ..user.forms import ChangeStatusForm
from ..user.forms.updatePriceList import UpdatePriceListForm

admin = Blueprint('admin', __name__)


@admin.route('/users')
@login_required
def users_page():
    user_request = User.query.join(Status, Status.status_id == User.status_id).add_columns(User.user_id, Status.status_id, Status.name, User.first_name, User.last_name, User.login).all()
    return render_template("admin/users.jinja2", title=f"Přehled uživatelů",
                           user_request=user_request)
@admin.route('/users/add', methods=['GET', 'POST'])
def add_user_page():
    form = AddUserForm()

    if form.validate_on_submit():
        new_user = User(
            form.first_name.data,
            form.last_name.data,
            form.telephone_number.data,
            form.login.data,
            form.password.data,
        )
        address = Address(
            form.street.data,
            form.house_number.data,
            form.city.data,
            form.zip_code.data
        )
        new_user.permanent_residence = address
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.view_login_page'))

    return render_template('admin/addUser.jinja2', title='Nový uživatel', form=form)


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
