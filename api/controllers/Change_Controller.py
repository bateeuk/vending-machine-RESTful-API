
# Import the classes
from models.Coin_Model import Coin_Model
from models.Change_Model import Change_Model

class Change_Controller():
    def __init__(self):
        self.cm = Change_Model()
        
    def view_change(self):
        # call the Change_Model to get the coin details from the database
        product_list = self.cm.get_change()

        # turn the db values into a key, value pair
        products = dict(product_list)

        return products

    def delete_change(self):
        self.cm.delete_change()

    def add_change(self):
        # grab the provided coin data from the request
        coin_model = Coin_Model()
        
        for coin, value in coin_model.coins.items():
            if value is not None:
                self.cm.add_change(value, coin)

