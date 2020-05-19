
# db interaction
from models.db_model import DB_Model

class Vend_Model():
    def __init__(self):
        self.db = DB_Model()
    
    def get_all_products(self):
        products = self.db.query_db_for_list('SELECT location, name, price, quantity FROM product')
        return products
        
    def get_product(self, location):
        product = self.db.query_db_for_list('SELECT location, name, price, quantity FROM product WHERE location = ? AND quantity > 0', (location,))
        return product

    def reduce_quantity(self, location):
        quantity = 1 #placeholder for future options of vending more than one item
        self.db.query_db_for_list('UPDATE product SET quantity = (quantity-?) WHERE location = ?', (quantity, location))