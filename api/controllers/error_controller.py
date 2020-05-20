
# to handle the HTTP errors
from werkzeug.exceptions import HTTPException

class Error_Controller():
    """
    Handles any raised exceptions

    ...
    Methods
    ----------
    handle(error:Exception)
        Formats errors as:
            { "message" : <description> }
            or if there is data:
            { "message" : description, "data": <returning_data> }
    """
    def handle(self, error):
        """
        Formats errors as:
        { "message" : <description> }
        or if there is data:
        { "message" : description, "data": <returning_data> }

        Parameters
        ----------
        error : Exception
            Error details, including message and error codes

        Returns
        ----------
        dict
            formatted error and error code
        """

        print ("An error occurred trying to process the request: ", end="")

        # Handle generated HTTP errors
        if isinstance(error, HTTPException):
            error_json = { "message" : error.description }
            print (error_json)
            return error_json, error.code
        
        # Handle custom errors:
        if len(error.args) >= 3:
            # Errors with additional data, such as refunds
            error_json = { "message" : error.args[1], "data" : error.args[2] }
            print (error_json)
            return error_json, error.args[0]
        elif len(error.args) == 2:
            # Errors with a message only
            error_json = { "message" : error.args[1] }
            print (error_json)
            return error_json, error.args[0]
        else:
            # Generic catch-all for unknown errors
            error_json = { "message" : error }, 500
            print (error_json)
            return error_json, 500