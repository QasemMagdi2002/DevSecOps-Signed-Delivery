# Demo Scenarios

This document outlines how to demonstrate the security capabilities of the pipeline.

---

## Scenario 1 — Signed Image Deployment (Allowed)

### Steps

* Deploy using:

  ```
  ghcr.io/qasemmagdi2002/devsecops-demo:latest
  ```

### Expected Result

* Pod starts successfully
* Kyverno allows the request

---

## Scenario 2 — Unapproved Image (Blocked)

### Steps

* Modify deployment to:

  ```
  image: nginx:latest
  ```

* Apply:

  ```
  kubectl apply -f k8s/deployment.yaml
  ```

### Expected Result

* Admission denied
* Kyverno blocks deployment

---

## Scenario 3 — Missing Resource Limits (Blocked)

### Steps

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
