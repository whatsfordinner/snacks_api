# Snacks API

A simple FLASK API to experiment with observability, metrics gathering and logging tools

## Design

The API is served by Flask and runs a SQLite DB

## Workflow

* A new snack can be created at `POST /snacks` but it must have a unique name 
* A list of all snacks can be returned with `GET /snacks`  
* A specific snack can be returned with `GET /snacks/:snackid`

## Lazy mode - TODO 

 When the API is lazy it will:
 |variable|values|purpose|
 |--------|------|-------|
 |`LAZY_WEB_SLOW`|`int` > 0|Web requests will be delayed by this many milliseconds +/- 10%|
 |`LAZY_WEB_ERROR`|0 <= `int` <= 100|Web methods will throw exceptions at this rate|
 |`LAZY_DB_SLOW`|`int` > 0|DB queries will have their responses delayed by this many milliseconds +/- 10%|
 |`LAZY_DB_ERROR`|0 <= `int` <= 100|DB requests will throw exceptions at this rate|
 |`LAZY_UTIL_SLOW`|`int` > 0|Utility requests (E.g. schema validation) will have their responses delayed by this many milliseconds +/- 10%|
 |`LAZY_UTIL_ERROR`|0 <= `int` <= 100|Utility requests will throw exceptions at this rate|


## Wishlist

If I get the basic bits working, I'd like to add:
* locust.io load testing
* switching data stores so comparative testing can be done  
* an auth workflow that involves a user registering and then hitting an auth endpoint to receive a JWT
