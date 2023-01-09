from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc

from .. import db
from ..admin.forms import AddPurchaseForm
from ..decorators import permission_required
from ..models import Permission, Purchase

purchase = Blueprint('purchase', __name__)


@purchase.route('/')
@login_required
def view_purchases_page():
    if current_user.is_administrator() or current_user.is_worker():
        purchases = Purchase.query.order_by(desc(Purchase.date)).all()
    else:
        purchases = Purchase.query \
            .filter_by(selling_customer_id=current_user.user_id) \
            .order_by(desc(Purchase.date)) \
            .all()

    return render_template("admin/purchases.jinja2", title=f"Přehled výkupů", purchases=purchases)


@purchase.route('/new', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.BUYING)
def view_add_purchase_page():
    form = AddPurchaseForm()

    # TODO: Change price
    if form.validate_on_submit():
        new_purchase = Purchase(
            form.weight.data,
            form.description.data,
            10,
            form.material_id.data.material_id,
            current_user.user_id,
            form.selling_customer_id.data.user_id
        )
        db.session.add(new_purchase)
        db.session.commit()

        return redirect(url_for('purchase.view_purchases_page'))

    return render_template("admin/addPurchase.jinja2", title=f"Přehled výkupů",
                           form=form)


@purchase.route('<int:id>')
@login_required
def view_purchase_detail_page(id: int):
    found_purchase = Purchase.query.get_or_404(id)
    data = dict(purchase=found_purchase)
    return render_template('purchase/detail.jinja2', title='Detail výkupu', data=data)
