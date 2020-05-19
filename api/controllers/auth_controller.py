
# Import reqparse to work with the provided login data
from flask_restful import reqparse

# Import jwt (JSON web token) and datetime for the token and expiration
import datetime, jwt

#import the classes
from models.auth_model import Auth_Model

class Auth_Controller:
    def __init__(self):
        self.am = Auth_Model()
        self.secretkey = '48oybc+s43"$^saF'
        self.ok = 'sdFs435guPaZ@9'

    def login(self):
        
        #setup a new RequestParser() to pick up the provided coin types and values
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="username cannot be blank!")
        parser.add_argument('password', required=True, help="password cannot be blank!")

        # Parse the arguments into an object
        login_obj = parser.parse_args()

        if self.am.login(login_obj) == False:
            return {'message': 'auth error' }, 401
        else:
            token = jwt.encode( { 'ok' : self.ok, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15) }, self.secretkey, algorithm='HS256' )
            return {'token': token.decode('UTF-8') }, 200

    def check_token(self):
        # get the token from the request
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help="token cannot be blank!")

        # Parse the arguments into an object
        token_obj = parser.parse_args()

        try:
            decoded_token = jwt.decode(token_obj['token'], self.secretkey, algorithms=['HS256'])
            if decoded_token['ok'] == self.ok:
                return {'message': 'check_token()', 'data': {}}, 200

        except:
            return {'message': 'missing or invalid token auth error' }, 401

        return {'message': 'auth error' }, 401