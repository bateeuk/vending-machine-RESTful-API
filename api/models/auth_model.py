
# Import bcrypt for password hashing
import bcrypt

# db interaction
from models.db_model import DB_Model

class Auth_Model:
    def login(self, login_obj):
        db = DB_Model()
        result = db.query_db_for_list('SELECT password FROM user WHERE username=?', (login_obj['username'],), one=True)

        if result is None:
            return False

        if bcrypt.checkpw(login_obj['password'].encode('utf-8'), result['password']):
            return True
        else:
            return False