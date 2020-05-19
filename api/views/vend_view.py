
# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Import the classes
from controllers.vend_controller import Vend_Controller

class Vend_View(Resource):
    def __init__(self):
        self.vc = Vend_Controller()

    def get(self, location):
        product = self.vc.view_product(location)
        if len(product) > 0:
            return product, 200
        else:
            return { "message": "Location not found" }, 404

    def post(self, location):
        product = self.vc.purchase_product(location)
        return product

