from flask import Blueprint

from .... import db
from ....models import User
from flask import Blueprint, render_template, flash

main = Blueprint('main', __name__)


class Statistics:
    m_user: User

    def __init__(self, user=None):
        self.m_user = user

    @staticmethod
    def get_price_list():
        return db.session.execute('''
    WITH recent_prices AS (SELECT p.price_id, p.material_id
                       FROM price_list p
                                JOIN (SELECT material_id, MAX(date) AS max_date
                                      FROM price_list
                                      GROUP BY material_id) m ON p.material_id = m.material_id AND p.date = m.max_date)
    SELECT price, name
    FROM recent_prices
         JOIN price_list ON recent_prices.price_id = price_list.price_id
         JOIN materials ON recent_prices.material_id = materials.material_id
    ORDER BY name ASC;
         ''').fetchall()

    @staticmethod
    def most_redeemed_material(self):
        return db.session.execute('''
        SELECT materials.name, max(count(materials.material_id))
        FROM materials 
        JOIN purchases ON (materials.material_id=purchases.material_id) 
        JOIN users ON (users.user_id=selling_customer_id)
        WHERE users.user_id = ? GROUP BY materials.name;
         ''', self.m_user.user_id).fetchall()

    def this_months_money(self):
        return db.session.execute(f'''
                    SELECT user_id, sum(price) 
                    FROM purchases 
                    JOIN users u on u.user_id = purchases.selling_customer_id 
                    WHERE EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM current_date) 
                    AND EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM current_date)
                    AND user_id = {self.m_user.user_id} 
                    GROUP BY user_id;''').fetchone()



    @main.route('/lives_money', methods='GET')
    def live_earnings(self):
        return db.session.execute('''
                SELECT sum(price)
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                JOIN purchases ON (materials.material_id=purchases.material_id)  
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? 
                 ''', self.m_user.user_id).fetchall()

    @main.route('/total_material', methods='GET')
    def total_bought_material(self, mat_name: str):
        return db.session.execute('''
                SELECT materials.name, sum(purchases.weight)
                FROM materials 
                JOIN purchases ON (materials.material_id=purchases.material_id) 
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? AND materials.name = ? 
                 ''', [self.m_user.user_id, mat_name]).fetchall()

    @main.route('/total', methods='GET')
    def total_bought(self):
        return db.session.execute('''
                    SELECT sum(purchases.weight)
                    FROM materials 
                    JOIN purchases ON (materials.material_id=purchases.material_id) 
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE users.user_id = ? AND materials.name = ?
                     ''', self.m_user.user_id).fetchall()

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
                    JOIN purchases ON (materials.material_id=purchases.material_id)  
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE purchases.date = GETDATE() 
                     ''').fetchall()

    @staticmethod
    def live_earnings_for_all_users():
        return db.session.execute('''
                    SELECT sum(price)
                    FROM price_list 
                    JOIN materials ON (materials.material_id=price_list.material_id)
                    JOIN purchases ON (materials.material_id=purchases.material_id)  
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
