
from .... import db
from ....models import User
from flask import Blueprint, render_template, flash

main = Blueprint('main', __name__)


class Statistics:
    m_user: User

    def __init__(self, user=None):
        self.m_user = user

    @main.route('/most_redeemed', methods='GET')
    def most_redeemed_material(self):
        request = db.session.execute('''
        SELECT materials.name, max(count(materials.material_id))
        FROM materials 
        JOIN purchases ON (materials.material_id=purchases.material_id) 
        JOIN users ON (users.user_id=selling_customer_id)
        WHERE users.user_id = ? GROUP BY materials.name;
         ''', self.m_user.user_id).fetchall()


    @main.route('/months_money', methods='GET')
    def this_months_money(self):
        data = db.session.execute('''
                SELECT sum(price_list.price) AS price
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                JOIN purchases ON (materials.material_id=purchases.material_id)  
                JOIN users ON (users.user_id=purchases.selling_customer_id)
                WHERE users.user_id = ?;
                 ''', self.m_user.user_id).fetchone()
        return render_template('user/dashboard.jinja2', data=data)


    @main.route('/lives_money', methods='GET')
    def live_earnings(self):
        return db.session.execute('''
                SELECT sum(price)
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                OIN purchases ON (materials.material_id=purchases.material_id)  
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
