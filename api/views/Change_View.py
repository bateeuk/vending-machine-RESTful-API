
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Import URL parser
from urllib.parse import urlparse, parse_qs

# Import classes
from controllers.Change_Controller import Change_Controller

class Change_View(Resource):
    def __init__(self):
        self.cc = Change_Controller()

    def get(self):
        change = self.cc.view_change()
        return change, 200

    def post(self):
        
        return {'message': 'POST within Change_View', 'data': {}}, 200

    def put(self):
        return {'message': 'PUT within Change_View', 'data': {}}, 200
