
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Import URL parser
from urllib.parse import urlparse, parse_qs

# Import classes
from controllers.change_controller import Change_Controller
from controllers.auth_controller import Auth_Controller

class Change_View(Resource):
    def __init__(self):
        self.cc = Change_Controller()
        self.ac = Auth_Controller()

    def get(self):
        self.ac.check_token()
        self.cc.get_available_change()
        return self.cc.cm.coins, 200

    def post(self):
        self.ac.check_token()
        self.cc.add_change()
        return {'message': 'POST within Change_View', 'data': {}}, 200

    def delete(self):
        self.ac.check_token()
        self.cc.delete_change()
        return {'message': 'delete within Change_View', 'data': {}}, 200
