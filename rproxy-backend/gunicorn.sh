#!/bin/bash

set -euo pipefail

export GUNICORN_BIND_ADDRESS=${GUNICORN_BIND_ADDRESS:-"0.0.0.0"}
export GUNICORN_BIND_PORT=${GUNICORN_BIND_PORT:-"8000"}
export GUNICORN_WORKERS=${GUNICORN_WORKERS:-"4"}
export GUNICORN_WORKER_CLASS=${GUNICORN_WORKER_CLASS:-"gevent"}
export GUNICORN_MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-"1000"}
export GUNICORN_MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JITTER:-"1000"}

exec gunicorn \
    --bind=${GUNICORN_BIND_ADDRESS}:${GUNICORN_BIND_PORT} \
    --workers=${GUNICORN_WORKERS} \
    --worker-class=${GUNICORN_WORKER_CLASS} \
    --max-requests=${GUNICORN_MAX_REQUESTS} \
    --max-requests-jitter=${GUNICORN_MAX_REQUESTS_JITTER} \
    --forwarded-allow-ips=* \
    --proxy-allow-from=* \
    "$@"