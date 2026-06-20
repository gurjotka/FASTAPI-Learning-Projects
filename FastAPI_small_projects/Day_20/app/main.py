# PROMETHEUS METRICS APP

from fastapi import FastAPI
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest
)
from fastapi.responses import Response
import time
import logging


app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total Requests",
    ["method", "endpoint"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Request duration"
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total Errors"
)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    REQUEST_COUNT.labels(
        request.method,
        request.url.path
    ).inc()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_DURATION.observe(duration)

    return response


@app.get("/")
def home():
    return {
        "message": "Hello"
    }


@app.get("/tasks")
def tasks():
    return [
        {"id": 1},
        {"id": 2}
    ]


@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )


@app.middleware("http")
async def metrics_middleware(request, call_next):

    try:
        response = await call_next(request)

        if response.status_code >= 400:
            ERROR_COUNT.inc()

        return response

    except Exception:
        ERROR_COUNT.inc()
        raise