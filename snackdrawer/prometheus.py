from flask import make_response
from prometheus_client import (
    Summary,
    Counter,
    multiprocess,
    generate_latest,
    CollectorRegistry,
    CONTENT_TYPE_LATEST
)

request_summary = Summary(
    'snackdrawer_api_requests',
    'Summary of REST API requests',
    ['endpoint', 'method']
)

db_summary = Summary(
    'snackdrawer_db_requests',
    'Summary of DB requests',
    ['query_type']
)

request_error_count = Counter(
    'snackdrawer_api_errors',
    'Count of REST API errors',
    ['endpoint', 'method']
)

auth_summary = Summary(
    'snackdrawer_auth_requests',
    'Summary of auth operations',
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
