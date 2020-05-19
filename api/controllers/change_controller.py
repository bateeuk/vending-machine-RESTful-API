
# Import request to work with the provided coin data
from flask import request

# Import the classes
from models.change_model import Change_Model

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
        if len(self.cm.coins['coins']) == 0:
            self.cm.get_change()

        acceptable_coins = self.cm.coins['coins']
        
        # pick up the provided coin types and values
        provided_coins = request.get_json()
        if provided_coins.get('coins') is None:
            print("Missing coins param")
            return { "error" : "Missing coins param" }, 400

        # check that all coins provided 
        for coin, value in provided_coins['coins'].items():
            if acceptable_coins.get(coin) is None:
                print("error invalid coin")
                return { "error" : "invalid coin" }, 400
            if type(value) is not int:
                print("error type error")
                return { "error" : "Coin values must be a whole number (integer)" }, 400

        self.cm.coins['coins'] = provided_coins['coins']
        self.cm.update_coin_value()

    def add_change(self):
        # grab the provided coin data from the request
        self.get_coins_from_request()
        for coin, value in self.cm.coins['coins'].items():
            if value is not None:
                self.cm.add_change(value, coin)

    def remove_change(self, quantity, coin):
        self.cm.remove_change(quantity, coin)


