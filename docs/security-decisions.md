# Security Decisions

This document explains the key security choices in this repository.

Each decision solves a real problem. Nothing here is random.

---

## Why Cosign Keyless Signing

Image signing is required.

There are two options:

- manage signing keys manually
- use keyless signing

Keyless signing is used.

Reasons:

- no key storage or rotation needed
- identity comes from GitHub OIDC
- reduces risk of key leakage
- signatures are verifiable through Sigstore

This keeps the system simple and secure.

---

## Why Kyverno (Not OPA/Gatekeeper)

Admission control is required.

Two main options:

- OPA / Gatekeeper
- Kyverno

Kyverno is used.

Reasons:

- uses native Kubernetes YAML
- no separate policy language
- easier to read and maintain
- faster to integrate into this setup

Policies stay close to the platform.

---

## Why Restrict Image Source

Containers should not come from anywhere.

Only approved registries are allowed.

Reasons:

- prevents pulling untrusted images
- blocks accidental use of public images
- reduces supply chain risk

If the source is not trusted, it is blocked.

---

## Why Require Signed Images

An image alone is not enough.

You must prove where it came from.

Signed images are enforced.

Reasons:

- verifies image origin
- ensures image was built by the pipeline
- blocks tampered images

No signature means no deployment.

---

## Why Enforce Digest-Based Deployment

Tags are mutable.

Digests are not.

Example:

- `:latest` can change at any time
- `@sha256:` always points to one exact image

Digest-based deployment is enforced.

Reasons:

- prevents image drift
- guarantees what was scanned is what runs
- improves traceability

---

## Why Require Resource Limits

Containers must define CPU and memory limits.

Reasons:

- prevents resource exhaustion
- ensures stable scheduling
- protects the cluster from noisy workloads

Without limits, one container can impact everything.

---

## Why Disallow Privileged Containers

Privileged containers bypass isolation.

Reasons:

- access to host-level resources
- increased attack surface
- harder to contain compromise

Privileged mode is blocked completely.

---

## Why Enforce Non-Root Execution

Containers should not run as root.

Reasons:

- limits impact of a compromise
- follows least-privilege principle
- aligns with modern container security practices

Each container runs with a defined user ID.

---

## Why Use Read-Only Root Filesystem

Containers should not modify their filesystem.

Reasons:

- prevents persistence of attacks
- blocks runtime tampering
- reduces writable surface

Only required paths (like `/tmp`) are writable.

---

## Why Use Trivy

A single tool is needed for multiple scans.

Trivy is used.

It covers:

- filesystem scanning
- container image vulnerabilities
- configuration issues

It simplifies the pipeline without losing coverage.

---

## Why Use Semgrep

Static analysis is required at the code level.

Semgrep is used.

Reasons:

- works out of the box
- supports multiple languages
- easy to run in CI

It catches issues before build.

---

## Why Use Syft for SBOM

An SBOM is required for visibility.

Syft is used.

Reasons:

- generates SBOM from container images
- supports standard formats
- integrates cleanly into CI

It shows exactly what is inside the image.

---

## Why Attach SBOM to the Image

An SBOM alone is not enough.

It must be tied to the image.

Reasons:

- prevents SBOM tampering
- creates a verifiable link
- ensures SBOM matches the deployed artifact

SBOM is attached using Cosign attestation.

---

## Why Skip metrics-server in Trivy

The metrics-server manifest exists only for local use.

It is not part of the application delivery path.

Scanning it adds noise without value.

So it is excluded.

---

## Summary

Each decision enforces one rule:

Only trusted, verified, and controlled workloads are allowed to run.

Everything else is blocked.