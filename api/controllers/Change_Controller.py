
# Import json for data formatting
import json

# Import the classes
from models.Change_Model import Change_Model

class Change_Controller():
    def __init__(self):
        self.cm = Change_Model()
        
    def view_change(self):
        # call the Change_Model to get the coin details from the database
        product_list = self.cm.get_change()

        # turn the db values into a key, value pair
        products = dict(product_list)

        return products


