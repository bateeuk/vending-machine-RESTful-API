
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
        self.secretkey = '48oybc+s43"$^saF'
        self.check_value = 'sdFs435guPaZ@9'

    def login(self) -> str:
        
        # Parse the arguments into an object to pick up the provided coin types and values
        login_obj = request.get_json()

        if 'username' not in login_obj.keys() or 'password' not in login_obj.keys():
            raise Exception(400,'Invalid or missing params')

        #salt used to encrypt the encoded message (self.check_value)
        salt = bcrypt.gensalt()
        auth_model = Auth_Model()
        encrypted_password_from_db = auth_model.login(login_obj['username'])
        if bcrypt.checkpw(login_obj['password'].encode('utf-8'), encrypted_password_from_db):
            hashed_check_value = bcrypt.hashpw(self.check_value.encode('utf-8'), salt)
            token = jwt.encode( { 'check_value' : hashed_check_value.decode('utf-8'), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15) }, self.secretkey, algorithm='HS256' )
            return token.decode('UTF-8')
        else:
            raise Exception(401,'Login unsuccessful')

    def check_token(self) -> bool:
        # get the token from the request
        token_obj = request.get_json()

        try:
            decoded_token = jwt.decode(token_obj['token'], self.secretkey, algorithms=['HS256'])
            if bcrypt.checkpw(self.check_value.encode('utf-8'), decoded_token['check_value'].encode('utf-8')) == False:
                raise Exception(401,'Authentication failed')
        except:
            raise Exception(401,'Missing or invalid token')
        else:
            return True
