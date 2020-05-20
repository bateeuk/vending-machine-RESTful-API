
# db interaction
from models.db_model import DB_Model

class Vend_Model():
    """
    Represents the products in the vending machine

    ...

    Attributes
    ----------
    db : DB_Model
        An instance of the DB_Model class (for handing database queries)
    product_list : list
        A list containing all product details (location, name, price, quantity)

    Methods
    -------
    get_all_products()
        Gets all products details (location, name, price, quantity) from the database (if the product(s) is in stock)
    get_product(location:str)
        Gets product details (location, name, price, quantity) for the specified product from the database (if the product is in stock)
    reduce_quantity(location:str)
        Reduce the number of products in the specified location by 1
    """
    def __init__(self):
        """ Initialises the DB_Model class """
        self.db = DB_Model()
        self.product_list = ()
    
    def get_all_products(self):
        """
        Assigns product_list to all products details (location, name, price, quantity) from the database (if the product(s) is in stock)
        """
        self.product_list = self.db.query_db_for_list('SELECT location, name, price, quantity FROM product WHERE quantity > 0')
        
    def get_product(self, location:str):
        """
        Assigns product_list to  product details (location, name, price, quantity) for the specified product from the database (if the product is in stock)
        
        Parameters
        ----------
        location : str
            The product's location
    
        """
        self.product_list = self.db.query_db_for_list('SELECT location, name, price, quantity FROM product WHERE location = ? AND quantity > 0', (location,))

    def reduce_quantity(self, location:str):
        """
        Reduce the number of products in the specified location by 1
        
        Parameters
        ----------
        location : str
            The product's location
        
        """
        self.db.query_db_for_list('UPDATE product SET quantity = (quantity-1) WHERE location = ?', (location,))