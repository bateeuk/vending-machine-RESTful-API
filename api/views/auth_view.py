
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Import the classes
from controllers.auth_controller import Auth_Controller
from controllers.error_controller import Error_Controller

class Auth_View(Resource):
    """
    Responsible for the formatting/display of the /login resource

    ...
    Attributes
    ----------
    error_controller : Error_Controller
        Handles any caught exceptions
    
    Methods
    ----------
    post()
        Formats the successful authentication (login).
        Calls the Error_Controller to format the error message if login is not successful
    """
    def __init__(self):
        """ Initialise the Error_Controller """
        self.error_controller = Error_Controller()

    def post(self):
        """
        Formats the successful authentication (login).
        Calls the Error_Controller to format the error message if login is not successful
            
        Returns
        ----------
        dict
            formatted success message with token and success HTTP code (200)
            If the login is not successful, call the Error_Controller to format the error message
        """
        try:
            auth_controller = Auth_Controller()
            token = auth_controller.login()
            return { 'message': 'Success', "data" : { 'token': token } }, 200
        except Exception as e:
            return self.error_controller.handle(e)


