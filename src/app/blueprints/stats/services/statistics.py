from typing import Dict, Any

from ....models import User, Purchase, Material, PriceList
from .... import db
from flask_login import current_user

class Statistics:
    m_user: User

    def __init__(self):
        if current_user.is_authenticated:
            self.m_user = current_user

    @staticmethod
    def most_redeemed_material():

        return db.execute('''
        SELECT materials.name, max(count(materials.material_id))
        FROM materials 
        JOIN purchases ON (materials.material_id=purchases.material_id) 
        JOIN users ON (users.user_id=selling_customer_id)
        WHERE users.user_id = ? GROUP BY materials.name
         ''', current_user.__getattribute__('user_id')).fetchall()

    @staticmethod
    def this_months_money():

        return db.execute('''
                SELECT sum(price)
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                OIN purchases ON (materials.material_id=purchases.material_id)  
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? AND purchases.date = GETDATE() 
                 ''', current_user.__getattribute__('user_id')).fetchall()

    @staticmethod
    def live_earnings():

        return db.execute('''
                SELECT sum(price)
                FROM price_list 
                JOIN materials ON (materials.material_id=price_list.material_id)
                OIN purchases ON (materials.material_id=purchases.material_id)  
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? 
                 ''', current_user.__getattribute__('user_id')).fetchall()

    @staticmethod
    def total_bought_material(mat_name: str):

        return db.execute('''
                SELECT materials.name, sum(purchases.weight)
                FROM materials 
                JOIN purchases ON (materials.material_id=purchases.material_id) 
                JOIN users ON (users.user_id=selling_customer_id)
                WHERE users.user_id = ? AND materials.name = ? 
                 ''', [current_user.__getattribute__('user_id'), mat_name]).fetchall()



    @staticmethod
    def total_bought():
        return db.execute('''
                    SELECT sum(purchases.weight)
                    FROM materials 
                    JOIN purchases ON (materials.material_id=purchases.material_id) 
                    JOIN users ON (users.user_id=selling_customer_id)
                    WHERE users.user_id = ? AND materials.name = ?
                     ''', current_user.__getattribute__('user_id')).fetchall()

