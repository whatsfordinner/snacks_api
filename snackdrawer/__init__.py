from logging.config import dictConfig
import os
from flask import Flask
from snackdrawer import db, drawers, errors, snacks, users
from snackdrawer.prometheus import export_metrics

# Taken mostly wholesale from the Flaskr tutorial
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    configure_logging()
    # TODO: need to make the DB backend switchable in future
    # TODO: need to be able to source config from environment
    app.config.from_mapping(
        SECRET_KEY='tasty_snacks',
        DATABASE=os.path.join(app.instance_path, 'snacks.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        # TODO: need to log fatally here
        pass

    db.init_app(app)
    db.init_db(app)

    errors.register_errors(app)

    app.register_blueprint(users.bp)
    app.register_blueprint(snacks.bp)
    app.register_blueprint(drawers.bp)

    app.add_url_rule('/metrics', 'metrics', export_metrics)

    return app

def configure_logging():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })
