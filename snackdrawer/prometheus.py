from flask import make_response
from prometheus_client import (
    Summary,
    Histogram,
    Counter,
    multiprocess,
    generate_latest,
    CollectorRegistry,
    CONTENT_TYPE_LATEST
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
