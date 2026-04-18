# Demo App

This folder contains a small FastAPI service used to demonstrate a production-style DevSecOps pipeline.

The application is intentionally simple. Its role is to act as the deployment target for security controls such as:

- static application security testing
- repository and container scanning
- SBOM generation
- image signing
- signed-image admission enforcement in Kubernetes
- secure deployment configuration

## Application Endpoints

### `GET /`
Returns general application metadata.

### `GET /health`
Basic health endpoint.

### `GET /ready`
Readiness endpoint for Kubernetes readiness probes.

### `GET /config`
Returns non-sensitive configuration values loaded from environment variables or Kubernetes ConfigMaps.

### `GET /secret-check`
Confirms whether a secret was injected into the application without exposing the secret value.

### `GET /cpu?iterations=500000`
Runs a controlled CPU-intensive loop to help demonstrate Horizontal Pod Autoscaler behavior.

## Environment Variables

The app supports the following variables:

- `APP_NAME`
- `APP_ENV`
- `APP_MESSAGE`
- `APP_SECRET`
- `APP_HOST`
- `APP_PORT`
- `APP_WORKERS`
- `APP_LOG_LEVEL`

## Local Development

Create and activate a virtual environment:

```bash
cd app
python -m venv .venv
source .venv/bin/activate