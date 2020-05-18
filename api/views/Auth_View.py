
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

class Auth_View(Resource):
    def post(self):
        return {'message': 'POST within Auth_View', 'data': {}}, 200
