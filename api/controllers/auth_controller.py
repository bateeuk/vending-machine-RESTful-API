
# Import request to pickup the provided login data
from flask import request

# Import jwt (JSON web token) and datetime for the token and expiration
import datetime, jwt

# Import bcrypt for hashing
import bcrypt

#import the classes
from models.auth_model import Auth_Model

class Auth_Controller:
    def __init__(self):
        self.am = Auth_Model()
        self.secretkey = '48oybc+s43"$^saF'
        self.ok = 'sdFs435guPaZ@9'

    def login(self):
        
        # Parse the arguments into an object to pick up the provided coin types and values
        login_obj = request.get_json()

        if 'username' not in login_obj.keys() or 'password' not in login_obj.keys():
            return {'message': 'invalid or missing params' }, 400

        #salt used to encrypt the encoded message (self.ok)
        salt = bcrypt.gensalt()

        if self.am.login(login_obj) == False:
            return {'message': 'auth error' }, 401
        else:
            hashed_ok = bcrypt.hashpw(self.ok.encode('utf-8'), salt)
            token = jwt.encode( { 'ok' : hashed_ok.decode('utf-8'), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15) }, self.secretkey, algorithm='HS256' )
            return {'token': token.decode('UTF-8') }, 200

    def check_token(self):
        # get the token from the request
        token_obj = request.get_json()

        try:
            #salt used to encrypt the encoded message (self.ok)
            salt = bcrypt.gensalt()
            decoded_token = jwt.decode(token_obj['token'], self.secretkey, algorithms=['HS256'])

            if bcrypt.checkpw(self.ok.encode('utf-8'), decoded_token['ok'].encode('utf-8')):
                return {'message': 'check_token()', 'data': {}}, 200
            else:
                return {'message': 'auth error' }, 401

        except:
            return {'message': 'missing or invalid token auth error' }, 401
