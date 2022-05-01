#!/bin/bash

set -euo pipefail

export CELERY_BEAT_SCHEDULE=${CELERY_BEAT_SCHEDULE:-"celery-beat-schedule"}
export CELERY_BEAT_LOGLEVEL=${CELERY_BEAT_LOGLEVEL:-"warning"}

exec celery \
    beat \
    -A "$@" \
    --schedule="${CELERY_BEAT_SCHEDULE}" \
    --loglevel="${CELERY_BEAT_LOGLEVEL}" \
    --pidfile=