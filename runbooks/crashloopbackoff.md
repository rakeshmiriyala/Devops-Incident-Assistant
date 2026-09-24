# CrashLoopBackOff

## What it means

`CrashLoopBackOff` means a container starts and then repeatedly exits.
Kubernetes progressively increases the delay between restart attempts.

## Common causes

- Application startup exception
- Missing environment variable
- Incorrect configuration
- Missing secret/config map
- Database connection failure
- Port or dependency configuration problem
- Application process exits immediately
- Resource constraints

## Investigation

```bash
kubectl get pods -A
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --tail=200
kubectl logs <pod-name> -n <namespace> --previous --tail=200
kubectl get events -A --sort-by=.lastTimestamp
```

## Important distinction

An incorrect container image generally produces:

```text
ErrImagePull
ImagePullBackOff
```

A `CrashLoopBackOff` requires evidence that the container actually started
and subsequently exited.
