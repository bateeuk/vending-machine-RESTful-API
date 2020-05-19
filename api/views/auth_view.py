
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Import the classes
from controllers.auth_controller import Auth_Controller

class Auth_View(Resource):
    def post(self):
        ac = Auth_Controller()
        return ac.login()


