

# db interaction
from models.DB_Model import DB_Model

class Change_Model():
    def __init__(self):
        self.db = DB_Model()
        self.coins = {}
        
    def get_change(self):
        change_list = self.db.query_db_as_is('SELECT coin, quantity FROM change_float')
        # turn the db values into a key, value pair
        self.coins = dict(change_list)
    
    def delete_change(self):
        self.db.query_db_for_list('UPDATE change_float SET quantity=0')
    
    def add_change(self, quantity, coin):
        self.db.query_db_for_list('UPDATE change_float SET quantity = (quantity+?) WHERE coin=?', (quantity, coin))

    def remove_change(self, quantity, coin):
        self.db.query_db_for_list('UPDATE change_float SET quantity = (quantity-?) WHERE coin=?', (quantity, coin))
