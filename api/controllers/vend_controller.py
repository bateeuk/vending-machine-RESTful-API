
# Import the classes
from models.vend_model import Vend_Model
from controllers.change_controller import Change_Controller

class Vend_Controller():
    def __init__(self):
        self.vend_model = Vend_Model()

    def view_all_products(self) -> list:
        # call the Vend_Model to get the product details from the database
        self.product_list = self.vend_model.get_all_products()
        return self.product_list

        
        if len(self.product_list) > 0:
            return self.product_list
        else:
            raise Exception(404,'The vending machine is currently empty')
        
    def view_product(self, location:str) -> list:
        # call the Vend_Model to get the product details from the database
        # turning location to uppercase as a precaution
        self.product_list = self.vend_model.get_product(location.upper())
        if len(self.product_list) > 0:
            return self.product_list
        else:
            raise Exception(404,'Location is empty or does not exist')

    def purchase_product(self, location:str):
        location = location.upper()
        self.product_list = self.vend_model.get_product(location)

        # grab the provided coin data from the request
        change_controller = Change_Controller()
        change_controller.get_coins_from_request()
        payment_coins = change_controller.change_model.coins['coins']
        payment_value = change_controller.change_model.coins['value']
        refund_json = { "change_returned": { "value": payment_value, "coins": payment_coins } }

        # Check if location exists
        if len(self.product_list) == 0:
            raise Exception(404,'Location does not exist', refund_json)

        # check there is enough to fulfill the request
        if self.product_list[0]['quantity'] == 0:
            raise Exception(404,'Product quantity is 0', refund_json)

        # check payment is enough to cover the price of the product
        # if not, issue full refund with Payment Required HTTP code
        if payment_value < self.product_list[0]['price']:
            raise Exception(402,'Product costs more than the money provided.', refund_json)

        total_refund_value = payment_value - self.product_list[0]['price']
        remaining_refund_value = payment_value - self.product_list[0]['price']

        coins_to_refund = {}

        for coin, num_in_float in change_controller.change_model.coins['coins'].items():
            # add the payment money to the float for use in returned coins
            num_in_float += payment_coins[coin]
            left_over = 0
            if num_in_float is not None:
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
            # add the payment money to the float
            change_controller.add_change()
            for coin, num in coins_to_refund.items():
                change_controller.remove_change(num,coin)

        # reduce number of product in stock
        self.vend_model.reduce_quantity(location)

        return { "change_returned": { "value": total_refund_value, "coins": coins_to_refund } }
