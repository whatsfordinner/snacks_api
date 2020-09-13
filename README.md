# Snacks API

A simple REST API to experiment with observability, metrics gathering and logging tools

## Running the API  
The Docker image is built using [Buildpacks](https://buildpacks.io/):

```
pack build \
--builder heroku/buildpacks:18 \
snackdrawer
```

After the image has been built, a `docker-compose` stack that includes Prometheus and Grafana can be run:
```
docker-compose -f local/docker-compose.yaml up -d
```

The API is accessible at: `http://localhost:8000`  
Prometheus is accessible at: `http://localhost:9090`  
Grafana is accessible at: `http://localhost:3000`

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
-u 20 -r 1 -t 2m --stop-timeout 10 \
-H http://localhost:8000
```

The loadtesting has a single, rudimentary type of user who will:
* Try and get lists of snacks  
* Create a new user account  
* Try and get their list of drawers  
* Try and create new drawers  
* Try and put snacks into their drawers  

If the user gets a `HTTP 401` they'll try and create a new JWT and attempt the task again. Once loadtesting is complete you'll see output showing the statistics of the test.

A pre-configured Grafana dashboard will show API performance statistics

## Prometheus Metrics

Prometheus metrics are exported on `/metrics`

## Wishlist

If I get the basic bits working, I'd like to add:
* fault injection with a lazy mode
* different sorts of users (E.g. poorly behaved users who try and access other users' data, script kiddies, etc.)  