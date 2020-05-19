
# Import reqparse to work with the provided coin data
from flask_restful import reqparse

# Import the classes
from models.Change_Model import Change_Model

class Change_Controller():
    def __init__(self):
        self.cm = Change_Model()
        
    def get_available_change(self):
        # call the Change_Model to get the coin details from the database
        self.cm.get_change()

    def delete_change(self):
        self.cm.delete_change()

    def get_coins_from_request(self):
        # if there isn't already one, setup the coins within the Change_Model as a basis for acceptable coin types
        if len(self.cm.coins) == 0:
            self.get_available_change()
        
        #setup a new RequestParser() to pick up the provided coin types and values
        parser = reqparse.RequestParser()
        for coin, value in self.cm.coins.items():
            parser.add_argument(coin, type=int, help='Coin values must be a whole number (integer)')

        # Parse the arguments into an object
        # strict=True means invalid coins are not accepted
        self.cm.coins = parser.parse_args(strict=True)

    def add_change(self):
        # grab the provided coin data from the request
        self.get_coins_from_request()
        
        for coin, value in self.cm.coins.items():
            if value is not None:
                self.cm.add_change(value, coin)
        
        # update the stored coins/float value
        self.cm.get_change()
    
    def get_coin_value(self):
        # Calculate the total value of the money provided (in pence, i.e. £1.43 becomes 143)
        coin_value = 0
        for coin, value in self.cm.coins.items():
            if value is not None:
                coin_value += int(coin) * value
        return coin_value

    def remove_change(self, quantity, coin):
        self.cm.remove_change(quantity, coin)


