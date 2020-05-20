
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Import URL parser
from urllib.parse import urlparse, parse_qs

# Import classes
from controllers.change_controller import Change_Controller
from controllers.auth_controller import Auth_Controller
from controllers.error_controller import Error_Controller

class Change_View(Resource):
    """
    Responsible for the formatting/display of the /float resource

    ...
    Attributes
    ----------
    error_controller : Error_Controller
        Handles any caught exceptions
    change_controller : Change_Controller
        Processes the change float
    auth_controller : Auth_Controller
        Ensures the user has successfully logged in / provided a valid token
    
    Methods
    ----------
    get()
        Formats the money stored in the change/float. 
        Calls the Error_Controller to format the error message if auth is not successful
    post()
        Calls the Change_Controller to add the provided change to the float. Formats the success message.
        Calls the Error_Controller to format the error message if auth is not successful
    delete()
        Calls the Change_Controller to empty out the float. Formats the success message.
        Calls the Error_Controller to format the error message if auth is not successful
    """
    def __init__(self):
        """ Initialise the Error_Controller, Change_Controller and Auth_Controller """
        self.error_controller = Error_Controller()
        try:
            self.change_controller = Change_Controller()
            self.auth_controller = Auth_Controller()
        except Exception as e:
            self.error_controller.handle(e)

    def get(self):
        """
        Formats the money stored in the change/float. 
        Calls the Error_Controller to format the error message if auth is not successful

        Returns
        ----------
        dict
            formatted success message, available coins from the float and success HTTP code (200)
            If the auth is not successful, call the Error_Controller to format the error message
        """
        try:
            if self.auth_controller.check_token() == True:
                self.change_controller.get_available_change()
                return { 'message': 'Success', "data" : self.change_controller.change_model.coins }, 200
        except Exception as e:
            return self.error_controller.handle(e)

    def post(self):
        """
        Calls the Change_Controller to add the provided change to the float.
        Calls the Error_Controller to format the error message if auth is not successful
        
        Returns
        ----------
        dict
            formatted success message and success HTTP code (200)
            If the auth is not successful, call the Error_Controller to format the error message
        """
        try:
            if self.auth_controller.check_token() == True:
                self.change_controller.add_change()
                return { 'message': 'Success' }, 200
        except Exception as e:
            return self.error_controller.handle(e)

    def delete(self):
        """
        Calls the Change_Controller to empty out the float.
        Calls the Error_Controller to format the error message if auth is not successful
        
        Returns
        ----------
        dict
            formatted success message, coins that were in the float are returned and success HTTP code (200)
            If the auth is not successful, call the Error_Controller to format the error message
        """
        try:
            if self.auth_controller.check_token() == True:
                self.change_controller.get_available_change()
                coins_to_return = self.change_controller.change_model.coins.copy()
                self.change_controller.delete_change()
                return { 'message': 'Success', "data" : coins_to_return }, 200
        except Exception as e:
            return self.error_controller.handle(e)
