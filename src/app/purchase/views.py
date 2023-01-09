from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required


from .. import db
from ..admin.forms import AddPurchaseForm
from ..decorators import permission_required
from ..models import User, Material, PriceList, Address, Role, Permission, Purchase


purchase = Blueprint('purchase', __name__)

@purchase.route('/')
@login_required

def purchases_page():
    if current_user.is_administrator() or current_user.is_worker():
        purchase_request = PriceList.query.join(Material, PriceList.material_id == Material.material_id).join(Purchase,
                                                                                                          Purchase.material_id == Material.material_id).join(
        User, Purchase.selling_customer_id == User.user_id).add_columns(User.first_name, User.last_name, Material.name,
                                                                        Purchase.weight, PriceList.price).all()
    else:
        purchase_request = PriceList.query.join(Material, PriceList.material_id == Material.material_id).join(Purchase,
                                                                                                              Purchase.material_id == Material.material_id).join(
            User, Purchase.selling_customer_id == User.user_id).add_columns(User.first_name, User.last_name,
                                                                            Material.name,
                                                                            Purchase.weight, PriceList.price, Purchase.selling_customer_id).filter_by(selling_customer_id = current_user.user_id).all()

    return render_template("admin/purchases.jinja2", title=f"Přehled výkupů",
                           purchase_request=purchase_request)


@purchase.route('/new', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.BUYING)
def purchases_add():
    form = AddPurchaseForm()

    if form.validate_on_submit():
        new_purchase = Purchase(
            form.weight.data,
            form.description.data,
            form.material_id.data.material_id,
            current_user.user_id,
            form.selling_customer_id.data.user_id
        )
        db.session.add(new_purchase)
        db.session.commit()

        return redirect(url_for('purchase.purchases_page'))

    return render_template("admin/addPurchase.jinja2", title=f"Přehled výkupů",
                           form=form)
