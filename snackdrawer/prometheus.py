from flask import make_response, request
from functools import wraps
from prometheus_client import (
    Summary,
    Histogram,
    Counter,
    Gauge,
    multiprocess,
    generate_latest,
    CollectorRegistry,
    CONTENT_TYPE_LATEST
)

request_gauge = Gauge(
    'active_api_requests',
    'Counter of active REST API requests',
    multiprocess_mode='livesum'
)

request_histogram = Histogram(
    'api_requests',
    'Histogram of REST API requests',
    ['endpoint', 'method']
)

request_error_count = Counter(
    'snackdrawer_api_errors',
    'Count of REST API errors',
    ['endpoint', 'method']
)

db_gauge = Gauge(
    'active_db_queries',
    'Counter of active DB queries',
    multiprocess_mode='livesum'
)

db_histogram = Histogram(
    'db_requests',
    'Histogram of DB requests',
    ['query_type']
)

auth_histogram = Histogram(
    'auth_requests',
    'Histogram of auth operations',
    ['operation']
)

def export_metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    response = make_response(
        data,
        200
    )
    response.headers = {
        'Content-Type': CONTENT_TYPE_LATEST,
        'Content-Length': str(len(data))
    }

    return response

def time_request(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        with request_histogram.labels(request.url_rule, request.method).time():
            with request_gauge.track_inprogress():
                return f(*args, **kwargs)
    return decorator

def time_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        with auth_histogram.labels(f.__name__).time():
            return f(*args, **kwargs)
    return decorator

def time_db(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        with db_histogram.labels(f.__name__).time():
            with db_gauge.track_inprogress():
                return f(*args, **kwargs)
    return decorator