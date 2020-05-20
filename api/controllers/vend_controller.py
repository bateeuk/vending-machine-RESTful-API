
# Import the classes
from models.vend_model import Vend_Model
from controllers.change_controller import Change_Controller

class Vend_Controller():
    """
    Handles the logic for vending products from the machine

    ...
    Attributes
    ----------
    vend_model : Vend_Model
        An instance of the Vend_Model class, which handles the database queries and stores the data
    
    Methods
    ----------
    view_all_products() -> list
        Calls the Vend_Model to generate a list of all products from the database.
        If one or more products exist, return them, otherwise raise a 404 exception
    view_product(location:str) -> list
        Calls the Vend_Model to generate details of the product in the specified location from the database.
        Return the product details if it exists, otherwise raise a 404 exception
    purchase_product(location:str) -> dict
        Calculates everything related to the purchase. Includes checking provided payment is enough, 
        that the float has enough money to cover any returned coins, and updates the database once purchase is complete.

    """
    def __init__(self):
        self.vend_model = Vend_Model()

    def view_all_products(self) -> list:
        """
        Calls the Vend_Model to generate a list of all products from the database.
        If one or more products exist, return them, otherwise raise a 404 exception

        Returns
        ----------
        list
            Product details (location, name, price and quantity)

        Raises
        ----------
        Exception
            If no products exist, raise 404 error. No products found
        """
        # call the Vend_Model to get the product details from the database
        self.vend_model.get_all_products()
        if len(self.vend_model.product_list) > 0:
            return self.vend_model.product_list
        else:
            raise Exception(404,'No products found: The vending machine is currently empty')
        
    def view_product(self, location:str) -> list:
        """
        Calls the Vend_Model to generate details of the product in the specified location from the database.
        Return the product details if it exists, otherwise raise a 404 exception

        Parameters
        ----------
        location : str
            The location of the product in the vending machine

        Returns
        ----------
        list
            Product details (location, name, price and quantity)

        Raises
        ----------
        Exception
            If product does not exist, raise 404 error. No products found
        """
        
        # turning location to uppercase as a precaution
        self.vend_model.get_product(location.upper())
        if len(self.vend_model.product_list) > 0:
            return self.vend_model.product_list
        else:
            raise Exception(404,'Location is empty or does not exist')

    def purchase_product(self, location:str) -> dict:
        """
        Calculates everything related to the purchase. Includes checking provided payment is enough, 
        that the float has enough money to cover any returned coins, and updates the database once purchase is complete.

        Parameters
        ----------
        location : str
            The location of the product in the vending machine

        Returns
        ----------
        dict
            Any money to be returned in coin type and number of coins (i.e. returning £0.52 could be { "50" : 1, "1" : 2 })

        Raises
        ----------
        Exception
            If location does not exist, raise 404 error.
            If product quantity is 0, raise 404 error.
            If not enough money has been provided for the purchase, raise a 402 error
            If the float doesn't contain enough coins to fulfill the coin return, raise a 503 error
        """
        location = location.upper()
        self.vend_model.get_product(location)

        # grab the provided coin data from the request
        change_controller = Change_Controller()
        change_controller.get_coins_from_request()
        payment_coins = change_controller.change_model.coins['coins']
        payment_value = change_controller.change_model.coins['value']
        refund_json = { "change_returned": { "value": payment_value, "coins": payment_coins } }

        # Check if location exists
        if len(self.vend_model.product_list) == 0:
            raise Exception(404,'Location does not exist', refund_json)

        # check there is enough to fulfill the request
        if self.vend_model.product_list[0]['quantity'] == 0:
            raise Exception(404,'Product quantity is 0', refund_json)

        # check payment is enough to cover the price of the product
        # if not, issue full refund with Payment Required HTTP code
        if payment_value < self.vend_model.product_list[0]['price']:
            raise Exception(402,'Product costs more than the money provided.', refund_json)

        total_refund_value = payment_value - self.vend_model.product_list[0]['price']
        remaining_refund_value = payment_value - self.vend_model.product_list[0]['price']


        # calculate the excat number of each coin to return once the purchase has been made
        coins_to_refund = {}
        for coin, num_in_float in change_controller.change_model.coins['coins'].items():
            # add the payment money to the float for use in returned coins
            num_in_float += payment_coins[coin]
            left_over = 0
            if num_in_float is not None:
                # calculate how many of this coin exist in the float
                # push remainder onto the next coin
                num_of_coin_needed = remaining_refund_value // int(coin) # calc how many of this coin are needed for refund
                if(num_in_float==0):
                    left_over = num_of_coin_needed
                elif(num_in_float < num_of_coin_needed):
                    if(num_of_coin_needed % num_in_float)==0:
                        left_over = num_of_coin_needed - num_in_float
                    else:
                        left_over = num_of_coin_needed % num_in_float
                else:
                    left_over = 0
                num_of_coin_to_provide = num_of_coin_needed - left_over
                value_of_coin_to_provide = num_of_coin_to_provide * int(coin)
                remaining_refund_value -= value_of_coin_to_provide
                coins_to_refund[coin] = num_of_coin_to_provide
                
        if remaining_refund_value > 0:
            raise Exception(503,'Not enough change in the float to process this request.', refund_json)
        else:
            # actually add the payment money to the float
            # then remove the refunded coins
            change_controller.add_change()
            for coin, num in coins_to_refund.items():
                change_controller.remove_change(num,coin)

        # reduce number of product in stock
        self.vend_model.reduce_quantity(location)

        return { "change_returned": { "value": total_refund_value, "coins": coins_to_refund } }
