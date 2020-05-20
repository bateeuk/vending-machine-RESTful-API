
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse


# Import the classes
from controllers.vend_controller import Vend_Controller
from controllers.error_controller import Error_Controller

class Vend_View(Resource):
    """
    Responsible for the formatting/display of the /product/<location> resource

    ...
    Attributes
    ----------
    error_controller : Error_Controller
        Handles any caught exceptions
    vend_controller : Vend_Controller
        Processes the purchasing of the product
    
    Methods
    ----------
    get()
        Formats the product for the location provided.  Formats the success message.
        Calls the Error_Controller to format the error message if product does not exist
        or another error occurs
    post()
        Calls the Vend_Controller to purchase the product specified. Formats the success message.
        Calls the Error_Controller to format the error message if product does not exist
        or another error occurs
    """
    def __init__(self):
        """ Initialise the Error_Controller and Vend_Controller """
        self.error_controller = Error_Controller()
        try:
            self.vend_controller = Vend_Controller()
        except Exception as e:
            self.error_controller.handle(e)

    def get(self, location:str):
        """
        Formats the product for the location provided.  Formats the success message.
        Calls the Error_Controller to format the error message if product does not exist
        or another error occurs

        Returns
        ----------
        dict
            formatted success message, available product details from the machine and success HTTP code (200)
            calls the Error_Controller to format the error message if the product location is empty
            or another error occurred
        """
        try:
            product = self.vend_controller.view_product(location)
            return { 'message': 'Success', "data" : product }, 200
        except Exception as e:
            return self.error_controller.handle(e)

    def post(self, location:str):
        """
        Calls the Vend_Controller to purchase the product specified. Formats the success message.
        Calls the Error_Controller to format the error message if product does not exist
        or another error occurs

        Returns
        ----------
        dict
            formatted success message, any refunded money from the purchase and success HTTP code (200)
            Calls the Error_Controller to format the error message if the product location is empty
            or another error occurred
        """
        try:
            refund = self.vend_controller.purchase_product(location)
            return { 'message': 'Success', "data" : refund }, 200
        except Exception as e:
            return self.error_controller.handle(e)
