# Image Startup Failure

## Symptoms

Common Kubernetes statuses:

- `ErrImagePull`
- `ImagePullBackOff`
- `InvalidImageName`

These normally indicate that Kubernetes cannot obtain or start the
requested container image.

## Example

Incorrect:

```text
myacr.azurecr.io/payment-ap:v5
```

Actual image:

```text
myacr.azurecr.io/payment-api:v5
```

The repository name differs by one character.

## Investigation

```bash
kubectl get pods -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe pod <pod-name> -n <namespace>
```

Look for messages such as:

```text
pull access denied
manifest unknown
repository does not exist
failed to resolve source
```

## Possible Fix

Correct the Deployment image:

```bash
kubectl set image deployment/payment-service \
  payment-service=myacr.azurecr.io/payment-api:v5 \
  -n payments
```

Then verify:

```bash
kubectl rollout status deployment/payment-service -n payments
kubectl get pods -n payments
```

The incident assistant does not execute mutation commands automatically.
An engineer should review and execute the change.
