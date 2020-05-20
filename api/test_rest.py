import requests
import json

base_url = 'http://localhost:5000'

def test_server_status():
    """
    Ensure we can reach the server
    """
    
    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    # Body
    payload = { }
    
    # convert dict to json by json.dumps() for body data. 
    resp = requests.get(base_url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers, e.g. status code.
    assert resp.status_code == 200

def test_login_success():
    url = base_url + "/login"

    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    # Body
    payload = {
        "username" : "jsmith",
        "password" : "Or4pgmT@sk"
        }
    
    # convert dict to json by json.dumps() for body data. 
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    print(resp.json())
    assert resp.status_code == 200

    """ TODO: pattern match the returned token """

def test_login_failure_incorrect_username():
    url = base_url + "/login"

    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    # Body
    payload = {
        "username" : "wrong",
        "password" : "Or4pgmT@sk"
        }
    
    # convert dict to json by json.dumps() for body data. 
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 401

def test_login_failure_incorrect_password():
    url = base_url + "/login"

    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    # Body
    payload = {
        "username" : "jsmith",
        "password" : "wrong"
        }
    
    # convert dict to json by json.dumps() for body data. 
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 401