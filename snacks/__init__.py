from logging.config import dictConfig
import os
from flask import Flask
from snacks import db, errors, routes

# Taken mostly wholesale from the Flaskr tutorial
def create_app():
    configure_logging()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='tasty_snacks',
        DATABASE=os.path.join(app.instance_path, 'snacks.sqlite'),
        LAZY_WEB_SLOW=os.getenv('LAZY_WEB_SLOW'),
        LAZY_WEB_ERROR=os.getenv('LAZY_WEB_ERROR'),
        LAZY_DB_SLOW=os.getenv('LAZY_DB_SLOW'),
        LAZY_DB_ERROR=os.getenv('LAZY_DB_ERROR'),
        LAZY_UTIL_SLOW=os.getenv('LAZY_UTIL_SLOW'),
        LAZY_UTIL_ERROR=os.getenv('LAZY_UTIL_ERROR')
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

def configure_logging():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s',
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