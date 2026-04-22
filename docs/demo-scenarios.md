# Demo Scenarios

This document shows how the system behaves in real situations. Each scenario proves that a specific control works.

---

## Scenario 1 — Signed Image Deployment

A properly built image is deployed. The CI pipeline runs, the image is scanned, an SBOM is generated, the image is signed, and deployment uses the image digest. As a result, the deployment succeeds, pods start normally, and the application responds correctly.

---

## Scenario 2 — Unsigned Image

An image without a signature is deployed. For example:

```yaml
image: ghcr.io/qasemmagdi2002/devsecops-demo@sha256:xxxx
```

But the image was never signed. Kyverno blocks the deployment, and no pods are created because signed image verification is required.

---

## Scenario 3 — Tag-Based Image

A tag is used instead of a digest. For example:

```yaml
image: ghcr.io/qasemmagdi2002/devsecops-demo:latest
```

Kyverno blocks the deployment because tags are mutable and not trusted. Only digest-based images are allowed.

---

## Scenario 4 — Untrusted Registry

An image from a different registry is deployed. For example:

```yaml
image: docker.io/library/nginx:latest
```

Kyverno blocks the deployment because only approved registries are allowed.

---

## Scenario 5 — Missing Resource Limits

A container is deployed without CPU or memory limits. For example:

```yaml
resources: {}
```

Kyverno blocks the deployment because all containers must define resource requests and limits.

---

## Scenario 6 — Privileged Container

A container is deployed with elevated privileges. For example:

```yaml
securityContext:
  privileged: true
```

Kyverno blocks the deployment because privileged containers are not allowed.

---

## Scenario 7 — Runtime Hardening

The application runs with strict security settings. Enforced settings include a non-root user, read-only root filesystem, and dropped Linux capabilities. The application runs normally, but the attack surface is reduced.

---

## Scenario 8 — HPA Scaling

The CPU endpoint is triggered:

```
/cpu?iterations=5000000
```

CPU usage increases, HPA scales the number of pods, and load is distributed.

---

## Scenario 9 — SBOM Generation

The pipeline generates an SBOM from the built image. The SBOM is stored as an artifact and reflects actual runtime dependencies.

---

## Scenario 10 — SBOM Attestation

The SBOM is attached to the image. The SBOM is linked to the image digest, and its integrity is verifiable.

---

## Summary

Each scenario shows one layer of control: CI blocks insecure code, build blocks vulnerable images, SBOM shows what is inside the image, signing proves image origin, admission blocks unsafe deployments, and runtime enforces safe execution. Nothing untrusted reaches the cluster.

* Remove resource requests/limits from deployment

### Expected Result

* Deployment rejected by Kyverno policy

---

## Scenario 4 — Privileged Container (Blocked)

### Steps

* Add:

  ```
  securityContext:
    privileged: true
  ```

### Expected Result

* Deployment denied

---

## Scenario 5 — Horizontal Scaling

### Steps

* Trigger load:

  ```
  curl "http://localhost:8080/cpu?iterations=100000000"
  ```

* Monitor:

  ```
  kubectl get hpa -n devsecops-demo -w
  ```

### Expected Result

* CPU usage increases
* replicas scale up

---
