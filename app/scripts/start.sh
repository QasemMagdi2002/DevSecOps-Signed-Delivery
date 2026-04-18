#!/usr/bin/env sh
set -eu

APP_MODULE="${APP_MODULE:-src.main:app}"
APP_HOST="${APP_HOST:-0.0.0.0}"
APP_PORT="${APP_PORT:-8000}"
APP_WORKERS="${APP_WORKERS:-1}"
APP_LOG_LEVEL="${APP_LOG_LEVEL:-info}"

case "$APP_PORT" in
    ''|*[!0-9]*)
        echo "APP_PORT must be a number" >&2
        exit 1
        ;;
esac

case "$APP_WORKERS" in
    ''|*[!0-9]*)
        echo "APP_WORKERS must be a number" >&2
        exit 1
        ;;
esac

if [ "$APP_WORKERS" -lt 1 ]; then
    echo "APP_WORKERS must be at least 1" >&2
    exit 1
fi

exec uvicorn "$APP_MODULE" \
    --host "$APP_HOST" \
    --port "$APP_PORT" \
    --workers "$APP_WORKERS" \
    --log-level "$APP_LOG_LEVEL"