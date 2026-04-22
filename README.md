# DevSecOps Signed Delivery Pipeline

This repository demonstrates how to secure a full software delivery pipeline. It goes beyond build and deploy by enforcing trust at every step. The pipeline follows this flow: Code → Build → Scan → SBOM → Sign → Attest → Deploy → Enforce. Only verified, signed, and compliant images are allowed to run.

---

## What This Repository Contains

The repository contains a production-style DevSecOps pipeline with:
- CI security checks (tests, SAST, scanning)
- container vulnerability scanning
- SBOM generation
- SBOM attestation
- keyless image signing using OIDC
- digest-based deployments
- Kubernetes admission control using Kyverno
- runtime security enforcement
- autoscaling with HPA

The application itself is simple—the pipeline is the focus.

---

## Architecture Overview

Here's how the system works:

1. Code is pushed to GitHub
2. GitHub Actions runs:
   - tests
   - Semgrep (SAST)
   - Trivy (filesystem + image scan)
3. Docker image is built
4. Image is scanned before push
5. SBOM is generated from the image
6. Image is pushed to GHCR
7. Image is signed using Cosign (keyless)
8. SBOM is attached to the image (attestation)
9. Kubernetes enforces:
   - allowed registry only
   - signed images only
   - digest-based images only
10. Application runs with strict runtime security
11. HPA scales based on load

---

## Key Security Controls

### CI Layer
- Semgrep scans the code
- Trivy scans the repository and configuration

### Build Layer
- Docker image is built securely
- vulnerabilities are blocked before push

### Artifact Layer
- SBOM is generated using Syft
- image is signed using Cosign
- SBOM is attached to the image

### Admission Layer
- Kyverno blocks:
  - unsigned images
  - tag-based images
  - untrusted registries

### Runtime Layer
- no privileged containers
- no root user
- read-only filesystem
- resource limits enforced

---

## Repository Structure

```
.github/workflows/   → CI/CD pipelines
app/                 → FastAPI service
k8s/                 → Kubernetes manifests
├── kyverno/       → security policies
├── local/         → metrics server setup
docs/                → documentation
```

---

## How to Run

### Run locally (Docker)
```bash
docker build -t devsecops-demo:local ./app
docker run -p 8000:8000 devsecops-demo:local
```

Open: http://localhost:8000/health

### Deploy to Kubernetes (manual)

1. Run the CI pipeline in GitHub
2. Download the rendered-k8s-manifest artifact
3. Apply it:

```bash
kubectl apply -f k8s/deployment.rendered.yaml
```

### Deploy using workflow (optional)

A separate deploy workflow is included. Provide:
- image digest
- enable deploy flag

This works when using a self-hosted runner or a reachable cluster.

---

## Why This Repository Matters

Most DevOps projects stop at deployment. This one enforces what gets built, what gets shipped, and what gets allowed to run. Every stage is verified.

---

## Status

**Completed:**
- CI security pipeline
- container scanning
- SBOM generation
- SBOM attestation
- image signing
- digest-only deployment
- Kyverno policy enforcement
- runtime hardening

**Next Steps:**
- SBOM-based admission policies
- vulnerability allowlisting (VEX)
- deployment promotion stages
- remote cluster automation

---

## Documentation

- [docs/demo-scenarios.md](docs/demo-scenarios.md)
- [docs/sbom-strategy.md](docs/sbom-strategy.md)
- [docs/security-decisions.md](docs/security-decisions.md)

---

## Summary

This repository does not just automate delivery—it secures it.