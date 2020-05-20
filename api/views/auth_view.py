
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Import the classes
from controllers.auth_controller import Auth_Controller
from controllers.error_controller import Error_Controller

class Auth_View(Resource):
    def __init__(self):
        self.error_controller = Error_Controller()

    def post(self):   
        try:
            auth_controller = Auth_Controller()
            token = auth_controller.login()
            return { 'message': 'Success', "data" : { 'token': token } }, 200
        except Exception as e:
            return self.error_controller.handle(e)


