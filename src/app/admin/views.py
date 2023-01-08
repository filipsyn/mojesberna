from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from .forms import AddUserForm, ChangeRoleForm
from .. import db
from ..decorators import permission_required

from ..models import User, Material, PriceList, Status, Address, Role, Permission
from ..user.forms import ChangeStatusForm
from ..user.forms.updatePriceList import UpdatePriceListForm

admin = Blueprint('admin', __name__)


@admin.route('/users')
@login_required
@permission_required(Permission.USER_ADMINISTRATION)
def users_page():
    user_request = User.query.join(Status, Status.status_id == User.status_id).add_columns(User.user_id,
                                                                                           Status.status_id,
                                                                                           Status.name, User.first_name,
                                                                                           User.last_name,
                                                                                           User.login).all()
    return render_template("admin/users.jinja2", title=f"Přehled uživatelů",
                           user_request=user_request)

@admin.route('/usersRole')
@login_required
@permission_required(Permission.CHANGE_ROLE)

def users_role_page():
    user_role_request = User.query.join(Role, Role.role_id == User.role_id).add_columns(User.user_id,
                                                                                           Role.role_id,
                                                                                           Role.name, User.first_name,
                                                                                           User.last_name,
                                                                                           User.login).all()
    return render_template("admin/userRole.jinja2", title=f"Přehled práv uživatelů",
                           user_role_request=user_role_request)




@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_WORKER)
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
@permission_required(Permission.CHANGE_ROLE)
def update_price(id):
    form = UpdatePriceListForm()
    price_to_update = PriceList.query.get_or_404(id)
    if request.method == "POST":
        price_to_update.price = request.form['price']
        try:
            db.session.commit()
            return redirect(url_for('user.dashboard_page'))
            return render_template("user/updatePriceList.jinja2", form=form, price_to_update=price_to_update)
        except:
            flash('Error')
            return render_template("user/updatePriceList.jinja2", form=form, price_to_update=price_to_update)
    else:
        return render_template("user/updatePriceList.jinja2", form=form, price_to_update=price_to_update)


@admin.route('/changeStatus/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.STATUS_CHANGING)
def change_status(id):
    form = ChangeStatusForm()
    status_to_change = User.query.get_or_404(id)
    if request.method == "POST":
        status_to_change.status_id = request.form['status_id']
        try:
            db.session.commit()
            return redirect(url_for('admin.users_page'))
            return render_template("user/changeStatus.jinja2", form=form, status_to_change=status_to_change)
        except:
            flash('Error')
            return render_template("user/changeStatus.jinja2", form=form, status_to_change=status_to_change)
    else:
        return render_template("user/changeStatus.jinja2", form=form, status_to_change=status_to_change)


@admin.route('/changeRole/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.CHANGE_ROLE)
def change_role(id):
    form = ChangeRoleForm()
    role_to_change = User.query.get_or_404(id)
    if request.method == "POST":
        role_to_change.role_id = request.form['role_id']
        try:
            db.session.commit()
            return redirect(url_for('admin.users_role_page'))
            return render_template("admin/changeRole.jinja2", form=form, role_to_change=role_to_change)
        except:
            flash('Error')
            return render_template("admin/changeRole.jinja2", form=form, role_to_change=role_to_change)
    else:
        return render_template("admin/changeRole.jinja2", form=form, role_to_change=role_to_change)
