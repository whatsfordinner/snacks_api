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

## Load Testing

Once the API is running, it can be load tested using [locust](https://locust.io/):

```
locust --headless \
-f loadtesting/locust.py \
--only-summary \
-u 20 -r 1 -t 2m --stop-timeout 10s \
-H http://localhost:8000
```

## Wishlist

If I get the basic bits working, I'd like to add:
* switching data stores so comparative testing can be done  
* fault injection with a lazy mode