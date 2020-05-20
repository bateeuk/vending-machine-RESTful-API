
# db interaction
from models.db_model import DB_Model

class Change_Model():
    """
    Represents the change float/coins data

    ...

    Attributes
    ----------
    db : DB_Model
        An instance of the DB_Model class (for handing database queries)
    coins : dictionary
        Stores coin types and quantity, plus the overall value of the assigned coins

    Methods
    -------
    get_change()
        Gets all coin names and quantities from the database
    update_coin_value()
        Calculates the total value of the money stored in coins (in pence, i.e. £1.43 becomes 143)
    delete_change()
        Sets the quantity for all coins to 0
    add_change()
        Increases the quantity (by the number of that provided) in the database for the provided coin
    remove_change()
        Decreases the quantity (by the number of that provided) in the database for the provided coin
    """
    def __init__(self):
        """ Initialises the DB_Model class, and sets the coins variable to a default state """
        self.db = DB_Model()
        self.coins = { "value" : 0, "coins" : {}}
        
    def get_change(self):
        """ Gets all coin names and quantities from the database """
        change_list = self.db.query_db_as_is('SELECT coin, quantity FROM change_float')
        # turn the db values into a key, value pair
        self.coins['coins'] = dict(change_list)
        self.update_coin_value()
    
    def update_coin_value(self):
        """ Calculates the total value of the money stored in coins (in pence, i.e. £1.43 becomes 143) """
        self.coins['value'] = 0
        for coin, value in self.coins['coins'].items():
            if value is not None:
                self.coins['value'] += int(coin) * value

    def delete_change(self):
        """ Sets the quantity for all coins to 0 """
        self.db.query_db_for_list('UPDATE change_float SET quantity=0')
        self.get_change()
    
    def add_change(self, quantity:int, coin:str):
        """ Increases the quantity (by the number of that provided) in the database for the provided coin
        
        Parameters
        ----------
        quantity : int
            The number of coins to increase by
        coin : str
            The type of coin to update
        
        """
        self.db.query_db_for_list('UPDATE change_float SET quantity = (quantity+?) WHERE coin=?', (quantity, coin))
        self.get_change()

    def remove_change(self, quantity:int, coin:str):
        """ Decreases the quantity (by the number of that provided) in the database for the provided coin
        
        Parameters
        ----------
        quantity : int
            The number of coins to reduce by
        coin : str
            The type of coin to update
        
        """
        self.db.query_db_for_list('UPDATE change_float SET quantity = (quantity-?) WHERE coin=?', (quantity, coin))
        self.get_change()