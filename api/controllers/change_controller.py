
# Import request to work with the provided coin data
from flask import request

# Import the classes
from models.change_model import Change_Model

class Change_Controller():
    """
    Handles the processing of the money for both purchases and float

    ...
    Attributes
    ----------
    change_model : Change_Model
        An instance of the Change_Model class, which handles the database queries and stores the data
    
    Methods
    ----------
    get_available_change()
        get number of each coin available from the Change_Model
    delete_change()
        call the Change_Model to set all coin quantities to 0
    get_coins_from_request()
        pickup the coins provided from the request and update the Change_Model with these values
    add_change()
        calls get_coins_from_request() then calls the Change_Model to update the coins in the database
    remove_change(quantity:int, coin:str)
        call the Change_Model to reduce the quantity of the specified coin in the database by the provided amount
    """
    def __init__(self):
        """ Initialises the Change_Model """
        self.change_model = Change_Model()
        
    def get_available_change(self):
        """ get number of each coin available from the Change_Model """
        self.change_model.get_change()

    def delete_change(self):
        """ call the Change_Model to set all coin quantities to 0 """
        self.change_model.delete_change()

    def get_coins_from_request(self):
        """
        pickup the coins provided from the request and update the Change_Model with these values

        Raises
        ----------
        Exception
            If `coins` is not provided in the request, raise a 400 error
            If a provided coin does not match the name of the coins in the database, raise a 400 error
            If the number of coins (quantity) is not an int, raise a 400 error
        """

        # if there isn't already one, setup the coins within the Change_Model as a basis for acceptable coin types
        if len(self.change_model.coins['coins']) == 0:
            self.change_model.get_change()

        acceptable_coins = self.change_model.coins['coins']
        
        # pick up the provided coin types and values
        provided_coins = request.get_json()
        if provided_coins.get('coins') is None:
            raise Exception(400,'Missing parameters')

        # check that all coins provided 
        for coin, quantity in provided_coins['coins'].items():
            if acceptable_coins.get(coin) is None:
                raise Exception(400,'Invalid coin provided')
            if type(quantity) is not int:
                raise Exception(400,'Invalid coin quantity. Coin quantities must be a whole number (integer)')

        self.change_model.coins['coins'] = provided_coins['coins']
        self.change_model.update_coin_value()

    def add_change(self):
        """ calls get_coins_from_request() then calls the Change_Model to update the coins in the database """
        # grab the provided coin data from the request
        self.get_coins_from_request()
        for coin, value in self.change_model.coins['coins'].items():
            if value is not None:
                self.change_model.add_change(value, coin)

    def remove_change(self, quantity:int, coin:str):
        """ call the Change_Model to reduce the quantity of the specified coin in the database by the provided amount """
        self.change_model.remove_change(quantity, coin)


