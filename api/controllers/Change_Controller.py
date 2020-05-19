
# Import reqparse to work with the provided coin data
from flask_restful import reqparse

# Import the classes
from models.Change_Model import Change_Model

class Change_Controller():
    def __init__(self):
        self.cm = Change_Model()
        
    def get_available_change(self):
        # call the Change_Model to get the coin details from the database
        change_dict = self.cm.get_change()
        return change_dict

    def delete_change(self):
        self.cm.delete_change()

    def get_coins_from_request(self):
        parser = reqparse.RequestParser()
        parser.add_argument('200', type=int, help='The value of the 200 coin is not a whole number')
        parser.add_argument('100', type=int, help='The value of the 100 coin is not a whole number')
        parser.add_argument('50', type=int, help='The value of the 50 coin is not a whole number')
        parser.add_argument('20', type=int, help='The value of the 20 coin is not a whole number')
        parser.add_argument('10', type=int, help='The value of the 10 coin is not a whole number')
        parser.add_argument('5', type=int, help='The value of the 5 coin is not a whole number')
        parser.add_argument('2', type=int, help='The value of the 2 coin is not a whole number')
        parser.add_argument('1', type=int, help='The value of the 1 coin is not a whole number')

        # Parse the arguments into an object
        self.cm.coins = parser.parse_args()

    def add_change(self):
        # grab the provided coin data from the request
        self.get_coins_from_request()
        
        for coin, value in self.cm.coins.items():
            if value is not None:
                self.cm.add_change(value, coin)
    
    def get_coin_value(self):
        # Calculate the total value of the money provided (in pence, i.e. £1.43 becomes 143)
        coin_value = 0
        for coin, value in self.cm.coins.items():
            if value is not None:
                coin_value += int(coin) * value
        return coin_value

    def remove_change(self, quantity, coin):
        self.cm.remove_change(quantity, coin)


