from ....models import User, Purchase, Material, PriceList
from .... import db
from flask_login import current_user
from flask import Blueprint

stats = Blueprint('stats', __name__)


class Statistics:
    m_user: User

    def __init__(self):
        if current_user.is_authenticated:
            self.m_user = current_user

    @stats.route('/most_redeemed', methods='GET')
    def most_redeemed_material(self):

        return db.execute('''
        SELECT materials.name, max(count(materials.material_id))
        FROM materials 
        JOIN purchases ON (materials.material_id=purchases.material_id) 
        JOIN users ON (users.user_id=selling_customer_id)
        WHERE users.user_id = ? GROUP BY materials.name
         ''', self.m_user.__getattribute__('user_id')).fetchall()

    @stats.route('/months_money', methods='GET')
    def this_months_money(self):

        return db.execute('''
                SELECT sum(price)
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                OIN purchases ON (materials.material_id=purchases.material_id)  
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? AND purchases.date = GETDATE() 
                 ''', self.m_user.__getattribute__('user_id')).fetchall()

    @stats.route('/lives_money', methods='GET')
    def live_earnings(self):

        return db.execute('''
                SELECT sum(price)
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                OIN purchases ON (materials.material_id=purchases.material_id)  
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? 
                 ''', self.m_user.__getattribute__('user_id')).fetchall()

    @stats.route('/total_material', methods='GET')
    def total_bought_material(self, mat_name: str):

        return db.execute('''
                SELECT materials.name, sum(purchases.weight)
                FROM materials 
                JOIN purchases ON (materials.material_id=purchases.material_id) 
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? AND materials.name = ? 
                 ''', [self.m_user.__getattribute__('user_id'), mat_name]).fetchall()

    @stats.route('/total', methods='GET')
    def total_bought(self):
        return db.execute('''
                    SELECT sum(purchases.weight)
                    FROM materials 
                    JOIN purchases ON (materials.material_id=purchases.material_id) 
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE users.user_id = ? AND materials.name = ?
                     ''', self.m_user.__getattribute__('user_id')).fetchall()

    @staticmethod
    def most_redeemed_material_for_all_users():
        return db.execute('''
            SELECT materials.name, max(count(materials.material_id))
            FROM materials 
            JOIN purchases ON (materials.material_id=purchases.material_id) 
            JOIN users ON (users.user_id=selling_customer_id)
             ''').fetchall()

    @staticmethod
    def this_months_money_for_all_users():
        return db.execute('''
                    SELECT sum(price)
                    FROM price_list 
                    JOIN materials ON (materials.material_id=price_list.material_id)
                    OIN purchases ON (materials.material_id=purchases.material_id)  
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE purchases.date = GETDATE() 
                     ''').fetchall()

    @staticmethod
    def live_earnings_for_all_users():
        return db.execute('''
                    SELECT sum(price)
                    FROM price_list 
                    JOIN materials ON (materials.material_id=price_list.material_id)
                    OIN purchases ON (materials.material_id=purchases.material_id)  
                    JOIN users ON (users.user_id=selling_customer_id)
                     ''').fetchall()

    @staticmethod
    def total_bought_material_for_all_users(mat_name: str):
        return db.execute('''
                    SELECT materials.name, sum(purchases.weight)
                    FROM materials 
                    JOIN purchases ON (materials.material_id=purchases.material_id) 
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE materials.name = ? 
                     ''', mat_name).fetchall()

    @staticmethod
    def total_bought_for_all_users_for_all_users():
        return db.execute('''
                        SELECT sum(purchases.weight)
                        FROM materials 
                        JOIN purchases ON (materials.material_id=purchases.material_id) 
                        JOIN users ON (users.user_id=selling_customer_id)
                        WHERE materials.name = ?
                         ''').fetchall()
