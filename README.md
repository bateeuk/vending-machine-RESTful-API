
# Vending Machine RESTful API
A RESTful implementation of a basic vending machine system

# Usage

There are four routes into this API:
- ```/login``` enables the user to receive a token for interacting with the float.
- ```/float``` allows the money in the machine to be manipulated. Requires a valid token from the /login route.
- ```/products``` view all of the products in the machine.
- ```/product``` view and purchase a single product in the machine

All other routes will receive a standard HTTP 404 error.

## /login

**Definition**

`POST /login` login to generate a valid token. The token can be used for actions on the change float.
The username and password provided in the example are valid on a default install.

**Arguments**
- `username:string` a valid username to authenticate
- `password:string` a valid password to authenticate

Example:
```json
{
	"username" : "jsmith",
	"password" : "Or4pgmT@sk"
}
```

**Response**

- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
- `401 Unauthorised` if username/password is not valid
- `200 OK` on success
```json
{
    "message": "Success",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaGVja192YWx1ZSI6IiQyYiQxMiRXb1MxeElEWXBkSDc4UXJaVEtkSW0uZVhpa2NVL1EzSkczdWU2eEdmUVU2emNOTEw0Mk85aSIsImV4cCI6MTU4OTk4ODIwN30.mJlmosCDQ4grjlPlLL3IAfUwogD_85sDD3ux7UsPUrQ"
    }
}
```

## /float
### Set the float (money held by the machine to provide change for purchases)

**Definition**

`POST /float` to add to the existing float with additional coins

**Arguments**
- `token:string` the token provided in response to `/login`
- `coins:JSON` detailing each coin denomination as its value in pennies, i.e. a £2 coin becomes "200", a 50p becomes "50" etc. and the number of those coins provided

Example:
```json
{
	"token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvayI6Im9rIiwiZXhwIjoxNTg5OTAwNDAyfQ.p40fA0hpOzEmcvQPeHF2BYZncF1OfLWwwEaxQ-bc1DU",
	"coins":
	{
		"200": 23,
		"100": 43,
		"50": 102,
		"20": 243,
		"10": 300,
		"5": 400,
		"2": 100,
		"1": 200
	}
}
```

**Response**

- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
- `401 Unauthorised` if token is not valid
- `200 OK` on success

**Definition**

`DELETE /float` to remove the float from the vending machine and return all coins

**Arguments**

- `token:string` the token provided in response to `/login`

Example:
```json
{
	"token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvayI6Im9rIiwiZXhwIjoxNTg5OTAwNDAyfQ.p40fA0hpOzEmcvQPeHF2BYZncF1OfLWwwEaxQ-bc1DU"
}
```

**Response**

- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
- `401 Unauthorised` if token is not valid
- `200 OK` on success

```json
{
    "message": "Success",
    "data": {
        "value": 24260,
        "coins": {
            "200": 23,
            "100": 43,
            "50": 102,
            "20": 243,
            "10": 300,
            "5": 400,
            "2": 100,
            "1": 200
        }
    }
}
```

### Lookup the current float details

**Definition**

`GET /float`

**Arguments**
- `token:string` a valid token for authentication

Example:
```json
{
	"token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

**Response**

- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
- `401 Unauthorised` if token is not valid
- `200 OK` on success

```json
{
    "message": "Success",
    "data": {
        "value": 24260,
        "coins": {
            "200": 23,
            "100": 43,
            "50": 102,
            "20": 243,
            "10": 300,
            "5": 400,
            "2": 100,
            "1": 200
        }
    }
}
```
## /products
### List all products

**Definition**

`GET /products`

**Response**

- `200 OK` on success

```json
{
    "message": "Success",
    "data": [
        {
            "location": "A1",
            "name": "Lindt Lindor Chocolate Treat Bar 38G",
            "price": 85,
            "quantity": 306
        },
        {
            "location": "A2",
            "name": "Mars Bar Single 51G",
            "price": 60,
            "quantity": 9
        },
        {
            "location": "B1",
            "name": "Cadbury Star Bar 49G",
            "price": 60,
            "quantity": 2
        }
}
```
## /product
### Lookup product details

**Definition**

`GET /product/<location>`

**Arguments**
- `"location":string` the product location within the vending machine (e.g. "A1")

**Response**

- `404 Not Found` the product location does not exist, or the location does exist but the product is not available (i.e. quantity of 0)
- `200 OK` on success

```json
{
    "message": "Success",
    "data": [
        {
            "location": "A1",
            "name": "Lindt Lindor Chocolate Treat Bar 38G",
            "price": 85,
            "quantity": 306
        }
    ]
}
```

### Purchase a product

**Definition**

`POST /product/<location>`

**Arguments**
- `location:string` the product location within the vending machine (e.g. "A1")
- `coins:JSON` detailing each coin denomination as its value in pennies, i.e. a £2 coin becomes "200", a 50p becomes "50" etc. and the number of those coins provided

Example:
```json
{
	"coins" : {
		"100": 1,
		"50": 1,
		"20": 2,
		"2": 1
	}
}
```

**Response**

- Errors with no response JSON
-- `400 Bad Request` one or more parameters is missing, or the data provided is invalid
-- `404 Not Found` the product location does not exist, or the location does exist but the product is not available (i.e. quantity of 0)

- Errors with response JSON
-- `402 Payment Required` the product location does exist but costs more than the money provided
```json
{
    "message": "Product costs more than the money provided.",
    "data": {
        "change_returned": {
            "value": 2,
            "coins": {
                "1": 2
            }
        }
    }
}
```
-- `503 Service Not Available` there is not enough money in the float to cover the change for the purchase
```json
{
    "message": "Not enough change in the float to process this request.",
    "data": {
        "change_returned": {
            "value": 400,
            "coins": {
                "200": 2
            }
        }
    }
}
```
- Success
-- `200 OK` if the product location exists and the product is available
```json
{
    "message": "Success",
    "data": {
        "change_returned": {
            "value": 135,
            "coins": {
                "100": 1,
                "50": 0,
                "20": 1,
                "10": 1,
                "5": 1
            }
        }
    }
}
```

## Design Decisions

Why:
- RESTful API
- Python
- Flask
- MVC
- JWT

Coins only, no notes or card payment
Left flexibility for notes by simply adding additional data to the database and Coin_Model

## Installation Instructions

#some setup commands:
docker-compose build
docker-machine start default
docker-machine create
docker-machine ls


docker-compose up
docker-compose down

#compile and run the source code
dockerbuild -t <name>
docker run -p 80:80 <name>
