
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse


# Import the classes
from controllers.vend_controller import Vend_Controller
from controllers.error_controller import Error_Controller

class Vend_View(Resource):
    def __init__(self):
        self.vend_controller = Vend_Controller()
        self.error_controller = Error_Controller()

    def get(self, location:str):
        try:
            product = self.vend_controller.view_product(location)
            return { 'message': 'Success', "data" : product }, 200
        except Exception as e:
            return self.error_controller.handle(e)

    def post(self, location:str):
        try:
            product = self.vend_controller.purchase_product(location)
            return { 'message': 'Success', "data" : product }, 200
        except Exception as e:
            return self.error_controller.handle(e)
