# DevSecOps Signed Delivery Pipeline (Production-Oriented Demo)

This project demonstrates a production-style DevSecOps pipeline that enforces security across the full software delivery lifecycle:

**Code → Build → Artifact → Admission → Runtime**

The system ensures that only **secure, signed container images** are allowed to run in Kubernetes.

---

## Key Features

* CI pipeline with automated testing
* SAST using Semgrep
* Repository and configuration scanning using Trivy
* Secure container image build and push to GHCR
* Keyless image signing using Cosign (OIDC-based)
* Kubernetes admission control using Kyverno
* Enforcement of:

  * signed images only
  * resource limits and requests
  * non-privileged containers
* Horizontal Pod Autoscaling (HPA) with live metrics

---

## Architecture Overview

High-level flow:

1. Developer pushes code
2. GitHub Actions runs:

   * tests
   * security scans (Semgrep, Trivy)
3. Docker image is built and pushed to GHCR
4. Image is signed using Cosign (keyless signing via GitHub OIDC)
5. Kubernetes (via Kyverno) enforces:

   * only approved image source
   * only signed images allowed
6. Application is deployed with secure runtime configuration
7. HPA scales based on CPU usage

---

## Tech Stack

* GitHub Actions (CI/CD)
* Docker + GHCR (registry)
* Cosign (image signing)
* Kyverno (policy enforcement)
* Kubernetes (Docker Desktop)
* FastAPI (demo app)
* Trivy (security scanning)
* Semgrep (SAST)

---

## Repository Structure

```
.github/workflows/   → CI/CD pipelines
app/                 → FastAPI demo service
k8s/                 → Kubernetes manifests
  ├── kyverno/       → security policies
  ├── local/         → local cluster components (metrics-server)
docs/                → project documentation
```

---

## Security Enforcement

This project enforces multiple layers of security:

### CI Layer

* SAST scanning (Semgrep)
* Dependency & config scanning (Trivy)

### Build Layer

* Secure Docker build
* Image pushed to GHCR

### Artifact Layer

* Image signed using Cosign (keyless)

### Admission Layer

* Kyverno verifies:

  * image source
  * signature validity

### Runtime Layer

* No privileged containers
* Resource limits required
* Read-only root filesystem
* Non-root execution

---

## Demo Scenarios

See: `docs/demo-scenarios.md`

Includes:

* signed image deployment (allowed)
* unsigned image deployment (blocked)
* policy enforcement examples
* HPA scaling demonstration

---

## Why This Project

Most DevOps projects stop at deployment.

This project demonstrates **enforced trust and security** across the delivery pipeline, which is a key requirement in modern production systems.

---

## Status

Core DevSecOps pipeline completed (Phases 1–5).

Next improvements:

* SBOM generation (Syft)
* image vulnerability scanning in pipeline
* digest-based deployment enforcement

---
