import json

# db interaction
from models.db_model import DB_Model

class Vend_Model():
    def __init__(self):
        self.db = DB_Model()
    
    def get_all_products(self):
        products = list()
        products = self.db.query_db('SELECT location, name, price, quantity FROM product')
        # products = json.dumps(my_query)
        # if(self.conn is not None):
        #     c = self.conn.cursor()
        #     c.execute('SELECT location, name, price, quantity FROM product')
        #     products = c.fetchall()
        #     c.close()
        return products
        
    def get_product(self, location):
        product = list()
        product = self.db.query_db('SELECT location, name, price, quantity FROM product WHERE location = ?', (location,))
            # c = self.conn.cursor()
            # param = (location, )
            # c.execute('SELECT location, name, price, quantity FROM product WHERE location = ?', param)
            # product = c.fetchall()
            # c.close()
        return product
