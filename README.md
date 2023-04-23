# Wenea task 🚗🔌

The wenea task is a Django application which implements an API to manage charge stations, as well as a websocket server 
to notify clients about the status of the stations.

### Architecture

The project is composed of three parts, each one running in a different container via docker-compose:

* Django webapp
* PostgreSQL database
* Redis server

### Third-party libraries

Some libraries have been used to reduce code complexity and simplify the development process:

* Django REST Framework, to implement the API
* Django Channels, to implement the websocket server
* pytest, to run the test suite

## Usage

To run the project, you need to have the [Docker](https://docs.docker.com/) daemon running. Then, you can run the
following command:

    docker-compose up

### API

The API endpoints will be available under http://localhost:8000/api/01/. You can test the endpoints using the 
[DRF browsable API](http://localhost:8000/api/01/chargepoints/) on the browser, or you can use an http client like curl 
or httpie.

```bash
# Get all charge points
curl -X GET http://localhost:8000/api/01/chargepoints/

# Create a new charge point
curl -X POST http://localhost:8000/api/01/chargepoints/ -H "Content-Type: application/json" -d '{"name": "CP1"}'

# Get a charge point
curl -X GET http://localhost:8000/api/01/chargepoints/1/

# Update a charge point
curl -X PUT http://localhost:8000/api/01/chargepoints/1/ -H "Content-Type: application/json" -d '{"name": "CP1", "status": "CHARGING"}'

# Delete a charge point
curl -X DELETE http://localhost:8000/api/01/chargepoints/1/
```

### Websocket server

To connect to the websocket, open a browser tab and go to http://localhost:8000/lobby/. Every time that a charge point 
status changes or it is entirely deleted, the websocket server will send a message to all the clients connected to the 
lobby. This behaviour can be tested by opening multiple tabs and checking that the notifications are received in all of 
them. 

## Tests

To run the test suite, run the following command:

    docker-compose run --rm web pytest
