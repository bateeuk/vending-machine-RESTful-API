
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
    def __init__(self):
        self.change_controller = Change_Controller()
        self.auth_controller = Auth_Controller()
        self.error_controller = Error_Controller()

    def get(self):
        try:
            if self.auth_controller.check_token() == True:
                self.change_controller.get_available_change()
                return { 'message': 'Success', "data" : self.change_controller.change_model.coins }, 200
        except Exception as e:
            return self.error_controller.handle(e)

    def post(self):
        try:
            if self.auth_controller.check_token() == True:
                self.change_controller.add_change()
                return { 'message': 'Success' }, 200
        except Exception as e:
            return self.error_controller.handle(e)

    def delete(self):
        try:
            if self.auth_controller.check_token() == True:
                self.change_controller.get_available_change()
                coins_to_return = self.change_controller.change_model.coins.copy()
                self.change_controller.delete_change()
                return { 'message': 'Success', "data" : coins_to_return }, 200
        except Exception as e:
            return self.error_controller.handle(e)
