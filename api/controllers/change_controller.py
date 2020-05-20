
# Import request to work with the provided coin data
from flask import request

# Import the classes
from models.change_model import Change_Model

class Change_Controller():
    def __init__(self):
        self.change_model = Change_Model()
        
    def get_available_change(self):
        # call the Change_Model to get the coin details from the database
        self.change_model.get_change()

    def delete_change(self):
        self.change_model.delete_change()

    def get_coins_from_request(self):
        # if there isn't already one, setup the coins within the Change_Model as a basis for acceptable coin types
        if len(self.change_model.coins['coins']) == 0:
            self.change_model.get_change()

        acceptable_coins = self.change_model.coins['coins']
        
        # pick up the provided coin types and values
        provided_coins = request.get_json()
        if provided_coins.get('coins') is None:
            raise Exception(400,'Missing parameters')

        # check that all coins provided 
        for coin, value in provided_coins['coins'].items():
            if acceptable_coins.get(coin) is None:
                raise Exception(400,'Invalid coin provided')
            if type(value) is not int:
                raise Exception(400,'Invalid coin value. Coin values must be a whole number (integer)')

        self.change_model.coins['coins'] = provided_coins['coins']
        self.change_model.update_coin_value()

    def add_change(self):
        # grab the provided coin data from the request
        self.get_coins_from_request()
        for coin, value in self.change_model.coins['coins'].items():
            if value is not None:
                self.change_model.add_change(value, coin)

    def remove_change(self, quantity:int, coin:str):
        self.change_model.remove_change(quantity, coin)


