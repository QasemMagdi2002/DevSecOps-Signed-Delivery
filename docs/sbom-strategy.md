# SBOM Strategy

## Overview

This repository uses an SBOM to track what is inside each container image. The goal is simple: you know exactly what runs in the cluster. The SBOM is generated from the final container image, stored as a CI artifact, attached to the image using Cosign, and linked to a specific image digest. This makes the supply chain traceable and verifiable.

## Why SBOM Matters

Most security issues do not come from your code. They come from dependencies, such as outdated libraries, indirect dependencies, and vulnerable base images. An SBOM solves this by letting you see everything inside the image, track vulnerable components, verify what was deployed, and integrate with security tools later. Without an SBOM, you are guessing. With an SBOM, you know.

## Tool Choice

### Syft

Syft is used to generate the SBOM because it is built for container analysis, works directly on images, supports standard formats, and is fast and easy to run in CI. It fits the pipeline without extra complexity.

## SBOM Scope

The SBOM is generated from the image, not the source code. The command used is:

```bash
syft <image> -o cyclonedx-json
```

This matters because source-based SBOMs miss OS packages, runtime dependencies, and layers added during build. Image-based SBOM shows what actually runs.

## Format Used

CycloneDX JSON is used because it is widely supported, easy to parse, and compatible with security platforms. This keeps the SBOM usable outside the pipeline.

## Pipeline Integration

SBOM generation happens inside CI. The steps are:

1. Build the image locally
2. Scan the image for vulnerabilities
3. Generate SBOM using Syft
4. Upload SBOM as an artifact
5. Push image to registry
6. Sign the image
7. Attach SBOM to the image

The SBOM always matches the image that gets deployed.

## SBOM Storage

The SBOM is saved as `sbom-cyclonedx.json` and uploaded as a GitHub Actions artifact. This allows auditing past builds, downloading SBOM per run, and debugging dependency issues.

## SBOM Attestation

The SBOM is attached to the image using Cosign with the command:

```bash
cosign attest \
  --predicate sbom-cyclonedx.json \
  --type cyclonedx \
  <image>@<digest>
```

This step is critical.

## Why Attestation Matters

Without attestation, the SBOM can be changed and there is no link between SBOM and image. With attestation, the SBOM is tied to the exact image digest, stored with the image in the registry, and verifiable through Sigstore. This creates a trust chain.

## Trust Model

The system uses keyless signing, GitHub OIDC identity, and Sigstore (Fulcio and Rekor). This means no long-lived keys are needed, identity comes from the workflow, and signatures are publicly verifiable.

## Best Practices Used

This strategy follows real-world practices by generating SBOM from the image, using a standard format, storing SBOM as an artifact, attaching SBOM to the image, and deploying using image digests. Each step reduces risk.

## Limitations

This setup does not yet include SBOM-based admission policies, vulnerability tracking over time, or exploitability analysis (VEX). The foundation is there, but enforcement can go further.

## Future Improvements

Next steps include blocking images without SBOM, integrating vulnerability tracking tools, adding VEX support, and enforcing SBOM validation at admission.

## Summary

The SBOM answers one question clearly: what is inside the image? And it proves the answer is correct.