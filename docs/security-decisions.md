# Security Decisions

This document explains key design decisions in the project.

---

## Why Cosign Keyless Signing

Cosign with GitHub OIDC eliminates the need to manage signing keys manually, reducing operational complexity and key leakage risk.

---

## Why Kyverno (not OPA/Gatekeeper)

Kyverno is Kubernetes-native and supports declarative policy enforcement without requiring a separate policy language.

---

## Why Restrict Image Source

To prevent unauthorized or untrusted images from being deployed, only approved image paths are allowed.

---

## Why Require Resource Limits

Ensures predictable scheduling and prevents resource exhaustion attacks.

---

## Why Disallow Privileged Containers

Privileged containers bypass kernel isolation and significantly increase attack surface.

---

## Why Skip metrics-server in Trivy

The metrics-server manifest is used only for local development and is not part of the application delivery path.

---

## Why Use readOnlyRootFilesystem

Prevents runtime modification of container filesystem, reducing persistence of attacks.

---
