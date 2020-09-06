# Snacks API

A simple FLASK API to experiment with observability, metrics gathering and logging tools

## Design

The API is served by Flask and runs a SQLite DB

## Workflow

* A list of all snacks can be returned with `GET /snacks/`  
* A specific snack can be returned with `GET /snacks/:snackid`  
* A new user can be created with at `POST /auth/users` but users must have a unique username  
* An existing user can get a JWT at `POST /auth/login`  
* A new snack can be created at `POST /snacks` but it must have a unique name (requires a JWT)  
* An existing user can view all their drawers at `GET /drawers/` (requires a JWT)  
* An existing user can create a new drawer at `POST /drawers/` but it must have a unique name (requires a JWT)  
* An existing user can view the contents of a specific drawer at `GET /drawers/:drawerid` (requires a JWT)  
* An existing user can add a snack to a drawer at `POST /drawers/:drawerid` (requires a JWT)  

## Load Testing - TODO

Once the API is running, it can be load tested using locust

## Wishlist

If I get the basic bits working, I'd like to add:
* locust.io load testing
* switching data stores so comparative testing can be done  
* fault injection with a lazy mode