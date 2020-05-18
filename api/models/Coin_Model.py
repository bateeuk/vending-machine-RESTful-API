
# Import reqparse to work with the provided coin data
from flask_restful import reqparse

class Coin_Model():
    def __init__(self):
        self.get_coins()

    def get_coins(self):
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
        self.coins = parser.parse_args()

    def get_coin_value(self):
        # Calculate the total value of the money provided (in pence, i.e. £1.43 becomes 143)
        coin_value = 0
        for coin, value in self.coins.items():
            if value is not None:
                coin_value += int(coin) * value
        return coin_value