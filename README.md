# Snacks API

A simple REST API to experiment with observability, metrics gathering and logging tools

## Running the API  
The Docker image is built using [Buildpacks](https://buildpacks.io/):

```
pack build --builder heroku/buildpacks:18 snackdrawer
```

After the image has been built, it can be run with:
```
docker run -p 8000:8000 snackdrawer
```

## Design

The API is powered by Flask and runs a SQLite DB

## API

The following endpoints are exposed:

* `/auth/login`
* `/auth/user`
* `/drawers/`
* `/snacks/`  

## Load Testing

Once the API is running, it can be load tested using [locust](https://locust.io/):

```
locust --headless \
-f loadtesting/locust.py \
--only-summary \
-u 20 -r 1 -t 2m --stop-timeout 10s \
-H http://localhost:8000
```

The loadtesting has a single, rudimentary type of user who will:
* Try and get lists of snacks  
* Create a new user account  
* Try and get their list of drawers  
* Try and create new drawers  
* Try and put snacks into their drawers  

If the user gets a `HTTP 401` they'll try and create a new JWT and attempt the task again. Once loadtesting is complete you'll see output showing the statistics of the test.

## Wishlist

If I get the basic bits working, I'd like to add:
* switching data stores so comparative testing can be done  
* fault injection with a lazy mode
* different sorts of users (E.g. poorly behaved users who try and access other users' data, script kiddies, etc.)  