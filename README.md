# Snacks API

A simple FLASK API to experiment with observability, metrics gathering and logging tools

## Design

The API is served by Flask and runs a SQLite DB

## Workflow

* A new snack can be created at `POST /snacks` but it must have a unique name 
* A list of all snacks can be returned with `GET /snacks`  
* A specific snack can be returned with `GET /snacks/:snackid`
* A new user can be created with at `POST /auth/users` but users must have a unique username
* An existing user can get a JWT at `POST /auth/login`

## Load Testing - TODO

Once the API is running, it can be load tested using locust

## Wishlist

If I get the basic bits working, I'd like to add:
* an auth workflow that involves a user registering and then hitting an auth endpoint to receive a JWT
* locust.io load testing
* switching data stores so comparative testing can be done  
* fault injection with a lazy mode