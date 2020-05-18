
# Import reqparse to work with the provided coin data
from flask_restful import reqparse

# Import the classes
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
        print ("purchase_product(self, location):")
        self.product_list = self.vm.get_product(location.upper())

        # Check if location exists
        if len(self.product_list) == 0:
            return { }, 404

        # check there is enough to fulfill the request
        if self.product_list[0]['quantity'] == 0:
            return { }, 404

        parser = reqparse.RequestParser()
        parser.add_argument('200', type=int, help='help msg for 200')
        parser.add_argument('100', type=int, help='help msg for 100')
        parser.add_argument('50', type=int, help='help msg for 50')
        parser.add_argument('20', type=int, help='help msg for 20')
        parser.add_argument('10', type=int, help='help msg for 10')
        parser.add_argument('5', type=int, help='help msg for 5')
        parser.add_argument('2', type=int, help='help msg for 2')
        parser.add_argument('1', type=int, help='help msg for 1')

        # Parse the arguments into an object
        payment_coins = parser.parse_args()
        
        # Calculate the total value of the money provided (in pence, i.e. £1.43 becomes 143)
        payment_value = 0
        for coin, value in payment_coins.items():
            if value is not None:
                payment_value += int(coin) * value

        # check payment
        if payment_value < self.product_list[0]['price']:
            return { "change_returned": { "value": payment_value, "coins": payment_coins } }, 402

        


        
