import markdown
import os
import shelve

# Import the Flask framework
from flask import Flask, g
from flask_restful import Resource, Api

# Import the classes
from views.change_view import Change_View
from views.auth_view import Auth_View
from views.vend_view import Vend_View
from views.products_view import Products_View

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

@app.route("/")
def index():
    """ Show the README file to provide suitable documentation on the usage of the API """

    try:
        # Open the README file
        with open('../README.md', 'r') as markdown_file:

            # Read the content of the file
            content = markdown_file.read()

            # Convert to HTML
            return markdown.markdown(content)
    except:
        return "Could not find the README file", 404

# For all other routes, load the respective classes
api.add_resource(Auth_View, '/login')
api.add_resource(Change_View, '/float')
api.add_resource(Products_View, '/products')
api.add_resource(Vend_View, '/product/<string:location>')