from flask import Blueprint, render_template, flash
from flask_login import current_user
from .. import db
from sqlalchemy.sql import select
from .forms.EditPriceForm import EditPriceForm
from ..models import Material, PriceList
from datetime import datetime, timedelta

main = Blueprint('main', __name__)


@main.route('/')
def view_home_page():
    data = {
        'stats': {
            'Noviny': 1200,
            'Železo': 980,
            'Měď': 375,
            'Hliník': 525,
            'Olovo': 692,
        },
        'prices': {
            'Noviny': 2.70,
            'Železo': 4.50,
            'Měď': 85,
            'Mosaz': 45,
            'Olovo': 20
        }
    }
    return render_template('main/homepage.jinja2', title='Domovská stránka', data=data)


@main.route('/greet')
def view_greeting_page():
    return render_template('main/greet.jinja2', title='Greeting', greeting='Hello')


@main.route('/prices')
def add_material_prices():

    price_query = db.session.execute(''' WITH recent_prices AS (SELECT p.price_id, p.material_id
                       FROM price_list p
                                JOIN (SELECT material_id, MAX(date) AS max_date
                                      FROM price_list
                                      GROUP BY material_id) m ON p.material_id = m.material_id AND p.date = m.max_date)
    SELECT price, name
    FROM recent_prices
         JOIN price_list ON recent_prices.price_id = price_list.price_id
         JOIN materials ON recent_prices.material_id = materials.material_id;''').fetchall()


    user = current_user

    return render_template('main/price_list.jinja2', title='Ceník', prices_request=price_query, user=user)


@main.route('/prices/edit', methods=['GET', 'POST'])
def edit_material_price():
    form = EditPriceForm()

    if form.validate_on_submit():

        new_price = PriceList(form.opts.data.material_id, form.price.data)
        db.session.add(new_price)
        db.session.commit()
        flash("Cena materiálu byla úspešně aktualizována", 'success')
    return render_template("main/EditPriceList.jinja2", form=form)



