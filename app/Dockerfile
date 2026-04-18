FROM python:3.13.13-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN apk add --no-cache build-base

COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

FROM python:3.13.13-alpine AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    APP_WORKERS=1 \
    APP_LOG_LEVEL=info

WORKDIR /app

RUN apk add --no-cache tini \
    && addgroup -g 10001 -S appgroup \
    && adduser -u 10001 -S -G appgroup -h /home/appuser appuser

COPY --from=builder /opt/venv /opt/venv
COPY --chown=10001:10001 src /app/src
COPY --chown=10001:10001 scripts/start.sh /app/scripts/start.sh

RUN chmod 0555 /app/scripts/start.sh

USER 10001:10001

EXPOSE 8000

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/app/scripts/start.sh"]