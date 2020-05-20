

# db interaction
from models.db_model import DB_Model

class Change_Model():
    def __init__(self):
        self.db = DB_Model()
        self.coins = { "value" : 0, "coins" : {}}
        
    def get_change(self):
        change_list = self.db.query_db_as_is('SELECT coin, quantity FROM change_float')
        # turn the db values into a key, value pair
        self.coins['coins'] = dict(change_list)
        self.update_coin_value()
    
    def update_coin_value(self):
        # Calculate the total value of the money provided (in pence, i.e. £1.43 becomes 143)
        self.coins['value'] = 0
        for coin, value in self.coins['coins'].items():
            if value is not None:
                self.coins['value'] += int(coin) * value

    def delete_change(self):
        self.db.query_db_for_list('UPDATE change_float SET quantity=0')
        self.coins = { "value" : 0, "coins" : {}}
    
    def add_change(self, quantity:int, coin:str):
        self.db.query_db_for_list('UPDATE change_float SET quantity = (quantity+?) WHERE coin=?', (quantity, coin))
        self.get_change()

    def remove_change(self, quantity:int, coin:str):
        self.db.query_db_for_list('UPDATE change_float SET quantity = (quantity-?) WHERE coin=?', (quantity, coin))
        self.get_change()
