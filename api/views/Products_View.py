
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Import the classes
from controllers.Vend_Controller import Vend_Controller

class Products_View(Resource):
    def __init__(self):
        self.vc = Vend_Controller()

    def get(self):
        products = self.vc.view_all_products()
        if len(products) > 0:
            return products, 200
        else:
            return { "message": "Vending machine is empty" }, 404

