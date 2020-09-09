import logging
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from snackdrawer import create_app
from prometheus_client import make_wsgi_app

def create_wsgi_app():
    app = create_app()
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    return app

application = create_wsgi_app()