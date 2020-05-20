
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from controllers.error_controller import Error_Controller

# Import the classes
from controllers.vend_controller import Vend_Controller

class Products_View(Resource):
    """
    Responsible for the formatting/display of the /products resource

    ...
    Attributes
    ----------
    error_controller : Error_Controller
        Handles any caught exceptions
    
    Methods
    ----------
    get()
        Formats the available products from the vending machine
        Calls the Error_Controller to format the error message if there are no products
        or another error occurred
    """
    def __init__(self):
        """ Initialise the Error_Controller """
        self.error_controller = Error_Controller()
    
    def get(self):
        """
        Formats the available products from the vending machine
        Calls the Error_Controller to format the error message if there are no products
        or another error occurred

        Returns
        ----------
        dict
            formatted success message, available products from the machine and success HTTP code (200)
            calls the Error_Controller to format the error message if there are no products
            or another error occurred
        """
        try:
            vend_controller = Vend_Controller()
            products = vend_controller.view_all_products()
            return { 'message': 'Success', "data" : products } , 200
        except Exception as e:
            return self.error_controller.handle(e)

