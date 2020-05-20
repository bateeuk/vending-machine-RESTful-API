
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from controllers.error_controller import Error_Controller

# Import the classes
from controllers.vend_controller import Vend_Controller

class Products_View(Resource):
    def __init__(self):
        self.error_controller = Error_Controller()
    
    def get(self):
        try:
            vend_controller = Vend_Controller()
            products = vend_controller.view_all_products()
            return { 'message': 'Success', "data" : products } , 200
        except Exception as e:
            return self.error_controller.handle(e)

