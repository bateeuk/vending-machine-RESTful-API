
# db interaction
from models.db_model import DB_Model

class Auth_Model:
    """
    A class used to handle authentication database access (i.e. checking user details in the database)
    """
    def login(self, username:str) -> str:
        """Takes the username and returns the matching password from the database

        Args:
            username: the username provided from Auth_Controller

        Returns:
            The encrypted password associated with the provided username, if any

        """
        db = DB_Model()
        encrypted_password_from_db = db.query_db_for_list('SELECT password FROM user WHERE username=?', (username,), one=True)

        return encrypted_password_from_db['password']