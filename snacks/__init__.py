import logging
import os
from flask import Flask
from snacks import db, errors, routes

# Taken mostly wholesale from the Flaskr tutorial
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='tasty_snacks',
        DATABASE=os.path.join(app.instance_path, 'snacks.sqlite'),
        LAZY_SNACKS=('LAZY_SNACKS' in os.environ)
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    db.init_db(app)

    errors.register_errors(app)

    app.register_blueprint(routes.bp)

    return app
