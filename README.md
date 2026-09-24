# DevOps Incident Assistant

A LangGraph-based DevOps incident assistant that combines:

- Local runbook retrieval
- Kubernetes read-only diagnostics
- LLM-based incident analysis
- Clear separation between observed evidence and inferred root cause

## Architecture

```text
User
  |
  v
main.py
  |
  v
LangGraph
  |
  +--> RAG node
  |      |
  |      +--> Local runbooks
  |
  +--> Kubernetes node
  |      |
  |      +--> kubectl get pods
  |      +--> kubectl get events
  |      +--> kubectl describe pod
  |      +--> kubectl logs
  |
  +--> Analysis node
         |
         +--> ChatOpenAI
                |
                v
          Incident Analysis
```

## Project Structure

```text
Devops-Incident-Assistant/
├── main.py
├── graph.py
├── tools.py
├── knowledge_base.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── models/
│   ├── __init__.py
│   └── state.py
├── nodes/
│   ├── __init__.py
│   ├── rag.py
│   ├── k8s.py
│   └── analysis.py
└── runbooks/
    ├── database_timeout.txt
    ├── memory_leak.txt
    ├── service_restart.txt
    ├── image_startup_failure.md
    └── crashloopbackoff.md
```

## Setup

### 1. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure OpenAI

Copy:

```text
.env.example
```

to:

```text
.env
```

Then set:

```text
OPENAI_API_KEY=your_key_here
```

Never commit `.env`.

### 4. Configure Kubernetes

Make sure:

```bash
kubectl version --client
kubectl get pods -A
```

work on the machine running the assistant.

The assistant uses read-only diagnostic commands only.

## Run

```bash
python main.py
```

Example:

```text
Ask Incident Question: payment-service pods are failing after a deployment
```

## Real-world example: incorrect image name

Suppose the Deployment contains:

```text
myacr.azurecr.io/payment-ap:v5
```

but the correct image is:

```text
myacr.azurecr.io/payment-api:v5
```

Kubernetes will commonly show:

```text
ErrImagePull
ImagePullBackOff
```

The assistant retrieves the image startup runbook, collects pod/event
evidence and asks the LLM to explain the likely cause and verification steps.

## Real-world example: CrashLoopBackOff

For:

```text
payment-service-7d9f6b8c7d-abc12   0/1   CrashLoopBackOff
```

the assistant checks:

```bash
kubectl describe pod ...
kubectl logs ...
kubectl logs --previous ...
kubectl get events ...
```

It then distinguishes confirmed evidence from possible causes.

## Security Notes

This project intentionally avoids automatically executing destructive
commands such as:

```bash
kubectl delete
kubectl apply
kubectl rollout restart
kubectl exec
```

The assistant is intended to diagnose first and let an engineer review
any remediation before changing production infrastructure.

## Future Improvements

- Embedding-based RAG with Chroma/FAISS/PGVector
- Azure/AWS Kubernetes integrations
- Slack/Teams incident notifications
- Prometheus/Grafana metrics
- GitHub/Azure DevOps deployment history
- LangSmith tracing and evaluation
- Human approval before remediation
- Automated incident ticket generation
