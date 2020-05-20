
# to handle the HTTP errors
from werkzeug.exceptions import HTTPException

class Error_Controller():
    def handle(self, error):
        # Handle generated HTTP errors
        if isinstance(error, HTTPException):
            return { "message" : error.description }, error.code
        
        if len(error.args) >= 3:
            return { "message" : error.args[1], "data" : error.args[2] }, error.args[0]
        elif len(error.args) == 2:
            return { "message" : error.args[1] }, error.args[0]
        else:
            return { "message" : error }, 500 # Unknown error