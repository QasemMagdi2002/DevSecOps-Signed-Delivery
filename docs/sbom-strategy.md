# SBOM Strategy (Software Bill of Materials)

## Overview

This project implements a **production-oriented SBOM strategy** as part of a secure software supply chain.

The goal is to ensure **full visibility, traceability, and integrity** of all dependencies included in the built container image.

The SBOM is:

- generated from the **final container image**
- stored as a **pipeline artifact**
- **cryptographically attested** using Cosign
- linked to the **exact image digest**

---

## Why SBOM Matters

Modern supply chain attacks (e.g., Log4Shell, dependency poisoning) often originate from:

- indirect dependencies
- outdated libraries
- vulnerable base images

An SBOM allows:

- auditing all components inside an artifact
- tracking vulnerable dependencies
- proving what was deployed in production
- enabling downstream security tools (VEX, Dependency-Track, etc.)

---

## Tooling Choice

### Syft (by Anchore)

Syft was selected because:

- purpose-built for SBOM generation
- supports container images, filesystems, and source
- integrates well with CI pipelines
- produces standard formats (CycloneDX, SPDX)
- widely adopted in production environments

---

## SBOM Scope: Image-Based (Not Source-Based)

The SBOM is generated from the **built container image**, not just the source code.

```bash
syft <image> -o cyclonedx-json