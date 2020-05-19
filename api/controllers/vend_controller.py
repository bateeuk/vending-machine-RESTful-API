
# Import the classes
from models.vend_model import Vend_Model
from controllers.change_controller import Change_Controller

class Vend_Controller():
    def __init__(self):
        self.vm = Vend_Model()

    def view_all_products(self):
        # call the Vend_Model to get the product details from the database
        self.product_list = self.vm.get_all_products()
        return self.product_list
        
    def view_product(self, location):
        # call the Vend_Model to get the product details from the database
        # turning location to uppercase as a precaution
        self.product_list = self.vm.get_product(location.upper())
        return self.product_list

    def purchase_product(self, location):
        location = location.upper()
        self.product_list = self.vm.get_product(location)

        # Check if location exists
        if len(self.product_list) == 0:
            return { }, 404

        # check there is enough to fulfill the request
        if self.product_list[0]['quantity'] == 0:
            return { }, 404

        # grab the provided coin data from the request
        change_controller = Change_Controller()
        change_controller.get_coins_from_request()
        payment_coins = change_controller.cm.coins['coins']
        payment_value = change_controller.cm.coins['value']

        print("payment coins: ", end="")
        print(change_controller.cm.coins)
        
        # check payment is enough to cover the price of the product
        # if not, issue full refund with Payment Required HTTP code
        if payment_value < self.product_list[0]['price']:
            return { "change_returned": { "value": payment_value, "coins": payment_coins } }, 402

        total_refund_value = payment_value - self.product_list[0]['price']
        remaining_refund_value = payment_value - self.product_list[0]['price']

        coins_to_refund = {}

        for coin, num_in_float in change_controller.cm.coins['coins'].items():
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
            print("issue full refund")
            return { "change_returned": { "value": payment_value, "coins": payment_coins } }, 503
        else:
            # add the payment money to the float
            change_controller.add_change()
            for coin, num in coins_to_refund.items():
                change_controller.remove_change(num,coin)

        # reduce number of product in stock
        self.vm.reduce_quantity(location)

        return { "change_returned": { "value": total_refund_value, "coins": coins_to_refund } }, 200
