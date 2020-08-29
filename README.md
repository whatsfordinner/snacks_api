# Snacks API

A simple FLASK API to experiment with observability, metrics gathering and logging tools

## Design

The API is served by Flask and runs a SQLite DB

## Workflow

* A new snack can be created at `POST /snacks` but it must have a unique name 
* A list of all snacks can be returned with `GET /snacks`  
* A specific snack can be returned with `GET /snacks/:snackid`

## Lazy mode  

The app can be made to be intentionally lazy by setting the environment variable `LAZY_SNACKS`. When the API is lazy it will:
* arbitrarily take longer to serve some requests (at a variety of points in the workflow)
* sometimes refuse to serve a request (and return a `HTTP 500`)  

## Wishlist

If I get the basic bits working, I'd like to add:
* switching data stores so comparative testing can be done  
* an auth workflow that involves a user registering and then hitting an auth endpoint to receive a JWT
