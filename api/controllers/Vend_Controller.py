

# Import the classes
from models.Coin_Model import Coin_Model
from models.Vend_Model import Vend_Model

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
        coin_model = Coin_Model()
        payment_coins = coin_model.coins
        payment_value = coin_model.get_coin_value()
        
        # check payment is enough to cover the price of the product
        if payment_value < self.product_list[0]['price']:
            return { "change_returned": { "value": payment_value, "coins": payment_coins } }, 402

        ##TODO handle payment etc.
        ##TODO calculate change

        self.vm.reduce_quantity(location)

        return {"msg":"done"}, 200
