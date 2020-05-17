
# Vending Machine RESTful API
A RESTful implementation of a basic vending machine system

## Usage

### Authenticate

**Definition**

`POST /login` login to generate a valid token. The token can be used for actions on the change float

**Arguments**
- `username:string` a valid username to authenticate
- `password:string` a valid password to authenticate

Example:
```json
{
	"username" : "",
	"password" : ""
}
```

**Response**

- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
- `401 Unauthorised` if token is not valid
- `200 OK` on success
```json
{
	"token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### Set the float (money held by the machine to provide change for purchases)

**Definition**

`PUT /float` to remove the existing float and set a new value with new coins
`POST /float` to add to the existing float with additional coins

**Arguments**
- `???`

Example:
```json
{
	"token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
	"coins":
	{
		100: 43,
		50: 102,
		20: 243,
		10: 300,
		5: 400
		2: 100,
		1: 200
	}
}
```

**Response**

- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
- `401 Unauthorised` if token is not valid
- `200 OK` on success

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
	"value": 72,
	"coins":
	{
		100: 12,
		50: 10,
		20: 43,
		10: 30,
		5: 40
		2: 10,
		1: 2
	}
}
```

### List all products

**Definition**

`GET /products`

**Response**

- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
- `200 OK` on success

```json
[
    {
        "location": "A1",
        "name": "Wispa Duo",
        "price": 120,
        "quantity": 12
    },
    {
        "location": "B2",
        "name": "Twix",
        "price": 70,
        "quantity": 0
    }
]
```

### Lookup product details

**Definition**

`GET /product/<location>`

**Arguments**
- `"location":string` the product location within the vending machine (e.g. "A1")

**Response**

- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
- `404 Not Found` if the product location does not exist
- `204 No Content` if the product location does exist but there is no product available
- `200 OK` on success

```json
{
	"name": "Wispa Duo",
	"price": 120,
	"quantity": 12
}
```

### Purchase a product

**Definition**

`POST /product/<location>`

**Arguments**
- `"location":string` the product location within the vending machine (e.g. "A1")

**PARAMS????**
- `"coins":array`

Example:
```json
{
	100: 1,
	50: 1,
	20: 2,
	2: 1
}
```

**TODO** finish coins desc/datatype

**Response**

- Errors with no response JSON
-- `204 No Content` if the product location does exist but there is no product available
-- `400 Bad Request` if one or more parameters is missing, or the data provided is invalid
-- `404 Not Found` if the product location does not exist
- Errors with response JSON
-- `402 Payment Required` if the product location does exist but costs more than the money provided
-- `503 Service Not Available` if there is not enough money in the float to cover the change for the purchase
```json
{
	"change_returned":
	{
		"value": 72,
		"coins":
		{
			50: 1,
			20: 2,
			2: 1
		}
	}
}
```
- Success
-- `200 OK` if the product location exists and the product is available
```json
{
	"product": "Wispa",
	"change_returned":
	{
		"value": 22,
		"coins":
		{
			20: 2,
			2: 1
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
