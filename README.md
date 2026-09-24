# DevOps Incident Assistant

A LangGraph-based DevOps incident assistant that combines:

* Local runbook retrieval
* Kubernetes read-only diagnostics
* Local LLM-based incident analysis using Ollama
* Clear separation between observed evidence and inferred root cause
* Safe, non-destructive Kubernetes investigation

---

# Architecture

```text
                         User
                           |
                           v
                        main.py
                           |
                           v
                       LangGraph
                           |
            +--------------+--------------+
            |              |              |
            v              v              v
         RAG Node      Kubernetes Node   Analysis Node
            |              |              |
            v              v              v
      Local Runbooks   kubectl tools    Ollama LLM
                           |           llama3.2 / qwen3
                           |
              +------------+------------+
              |
              +--> get pods
              +--> get events
              +--> describe pod
              +--> pod logs
                           |
                           v
                  Incident Analysis
```

## Request Flow

```text
User Incident Question
        |
        v
    RAG Node
        |
        +--> Search local runbooks
        |
        v
 Kubernetes Node
        |
        +--> kubectl get pods
        +--> kubectl get events
        +--> kubectl describe pod
        +--> kubectl logs
        |
        v
 Analysis Node
        |
        +--> Local Ollama LLM
        |
        v
 Incident Analysis
        |
        +--> Incident Classification
        +--> Root Cause
        +--> Evidence
        +--> Recommended Fix
        +--> Verification Steps
        +--> Preventive Measures
```

---

# Project Structure

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
│
├── models/
│   ├── __init__.py
│   └── state.py
│
├── nodes/
│   ├── __init__.py
│   ├── rag.py
│   ├── k8s.py
│   └── analysis.py
│
└── runbooks/
    ├── database_timeout.txt
    ├── memory_leak.txt
    ├── service_restart.txt
    ├── image_startup_failure.md
    └── crashloopbackoff.md
```

---

# Technology Stack

| Component         | Technology                            |
| ----------------- | ------------------------------------- |
| Language          | Python                                |
| Agent Framework   | LangGraph                             |
| LLM Framework     | LangChain                             |
| Local LLM Runtime | Ollama                                |
| LLM               | `llama3.2:latest` / `qwen3:8b`        |
| Kubernetes        | kubectl                               |
| RAG               | Local keyword-based runbook retrieval |
| Infrastructure    | Kubernetes                            |
| Environment       | Linux / WSL / Windows                 |

---

# Prerequisites

Install the following before running the project:

* Python 3.10+
* Git
* Kubernetes `kubectl`
* A configured Kubernetes cluster
* Ollama
* A locally available Ollama model

The project can run without an OpenAI API key.

---

# Setup

## 1. Clone the Repository

```bash
git clone https://github.com/rakeshmiriyala/Devops-Incident-Assistant.git
cd Devops-Incident-Assistant
```

## 2. Create a Python Virtual Environment

### Linux / WSL / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

in your terminal.

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Current dependencies:

```text
langchain-core
langgraph
langchain-ollama
python-dotenv
```

---

# Ollama Configuration

This project uses **Ollama** instead of OpenAI.

Therefore, an OpenAI API key is not required.

## 1. Install Ollama

Verify the installation:

```bash
ollama --version
```

## 2. Pull an LLM

The project can use:

```bash
ollama pull llama3.2
```

or:

```bash
ollama pull qwen3:8b
```

Check installed models:

```bash
ollama list
```

Example:

```text
NAME               SIZE
llama3.2:latest    2.0 GB
qwen3:8b           5.2 GB
```

---

# Running Ollama with WSL

If the Python application runs inside WSL while Ollama runs on Windows, configure Ollama to accept connections from WSL.

Open **Windows PowerShell**:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
ollama serve
```

Keep this PowerShell window running.

Ollama should show something similar to:

```text
OLLAMA_HOST:http://0.0.0.0:11434
Listening on [::]:11434
```

## Find the WSL Gateway

From WSL:

```bash
ip route
```

Example:

```text
default via 172.20.0.1 dev eth0
```

In this example, Ollama can be reached through:

```text
http://172.20.0.1:11434
```

## Test Ollama Connectivity

From WSL:

```bash
curl http://172.20.0.1:11434/api/tags
```

If successful, the response contains the installed models.

For example:

```json
{
  "models": [
    {
      "name": "qwen3:8b"
    },
    {
      "name": "llama3.2:latest"
    }
  ]
}
```

---

# Configure the LLM

The LLM configuration is located in:

```text
graph.py
```

Example using `llama3.2`:

```python
llm = ChatOllama(
    model="llama3.2:latest",
    base_url="http://172.20.0.1:11434",
    temperature=0,
)
```

Example using Qwen3:

```python
llm = ChatOllama(
    model="qwen3:8b",
    base_url="http://172.20.0.1:11434",
    temperature=0,
)
```

If Ollama and the Python application are running on the same machine, the base URL can generally be:

```text
http://localhost:11434
```

---

# Test Ollama

Before running the complete application, test the LLM connection:

```bash
python -c "from langchain_ollama import ChatOllama; llm=ChatOllama(model='llama3.2:latest', base_url='http://172.20.0.1:11434', temperature=0); print(llm.invoke('What is Kubernetes? Answer in two sentences.').content)"
```

A successful response confirms:

```text
Python
  |
  v
LangChain
  |
  v
Ollama
  |
  v
Local LLM
```

is working.

---

# Kubernetes Configuration

The assistant uses `kubectl` for read-only diagnostics.

Verify `kubectl`:

```bash
kubectl version --client
```

Verify cluster connectivity:

```bash
kubectl get pods -A
```

Check the current Kubernetes context:

```bash
kubectl config current-context
```

List available contexts:

```bash
kubectl config get-contexts
```

---

# Kubernetes Diagnostic Tools

The assistant currently uses read-only Kubernetes commands.

## Get Pods

```bash
kubectl get pods -A -o wide
```

## Get Events

```bash
kubectl get events -A --sort-by=.lastTimestamp
```

## Describe a Pod

```bash
kubectl describe pod <pod-name> -n <namespace>
```

## Get Pod Logs

```bash
kubectl logs <pod-name> -n <namespace> --tail=200
```

## Get Previous Container Logs

```bash
kubectl logs <pod-name> -n <namespace> --previous --tail=200
```

---

# Run the Application

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the assistant:

```bash
python main.py
```

The application asks:

```text
Ask Incident Question:
```

Example:

```text
Payment service is failing after deployment. Investigate the incident.
```

The assistant then:

1. Receives the incident question
2. Searches local runbooks
3. Collects Kubernetes pod information
4. Collects Kubernetes events
5. Identifies the affected pod
6. Collects pod description
7. Collects pod logs
8. Sends the evidence to Ollama
9. Generates an incident analysis

---

# Sample Result

The following is an example of the application running against the intentionally broken `payment-service` deployment.

## Input

```text
Ask Incident Question: Payment service is failing after deployment. Investigate the incident.
```

## Kubernetes Test

The deployment uses an intentionally invalid image:

```yaml
image: nginx-does-not-exist:999
```

This is designed to simulate an image-pull failure.

## Application Output

```text
======================================================================
DEVOPS INCIDENT ANALYSIS
======================================================================

Incident Analysis

1. Incident Classification

Failed Image Pull / ImagePullBackOff incident.

2. Root Cause

The payment-service pod is unable to pull the configured
container image:

nginx-does-not-exist:999

The image reference is invalid or the image is unavailable
from the configured container registry.

3. Evidence

- The payment-service pod is failing during container startup.
- Kubernetes reports an image-pull failure.
- The configured image is:
  nginx-does-not-exist:999
- Kubernetes may transition the container through:
  ErrImagePull
  ImagePullBackOff

4. Recommended Fix

Verify the container image name and tag.

Check the pod events:

kubectl describe pod <pod-name> -n payments

Verify that:

- The image repository exists.
- The image tag exists.
- The registry is reachable.
- Required registry authentication is configured.

5. Verification Steps

kubectl get pods -n payments

kubectl describe pod <pod-name> -n payments

kubectl get events -n payments --sort-by=.lastTimestamp

After the image reference is corrected, verify that the pod
reaches Running status.

6. Preventive Measures

- Validate container image names during CI/CD.
- Validate image tags before deployment.
- Use immutable image tags.
- Add deployment validation to the pipeline.
- Verify container registry authentication.
```

> **Note:** LLM output can vary between runs. The result above represents the expected diagnostic reasoning for the intentionally invalid image test.

---

# Real-World Example: ImagePullBackOff

Consider a Deployment containing:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: payment-service
  namespace: payments

spec:
  replicas: 2

  selector:
    matchLabels:
      app: payment-service

  template:
    metadata:
      labels:
        app: payment-service

    spec:
      containers:
        - name: payment-service
          image: nginx-does-not-exist:999
          ports:
            - containerPort: 80
```

Because the image does not exist, Kubernetes may report:

```text
ErrImagePull
```

followed by:

```text
ImagePullBackOff
```

Investigate using:

```bash
kubectl get pods -A -o wide
```

```bash
kubectl get events -A --sort-by=.lastTimestamp
```

Then:

```bash
kubectl describe pod <pod-name> -n payments
```

The assistant combines this Kubernetes evidence with the relevant runbook and asks the local LLM to analyze the incident.

---

# Real-World Example: CrashLoopBackOff

A true `CrashLoopBackOff` occurs when a container starts but repeatedly terminates.

Example:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: payment-service
  namespace: payments

spec:
  replicas: 1

  selector:
    matchLabels:
      app: payment-service

  template:
    metadata:
      labels:
        app: payment-service

    spec:
      containers:
        - name: payment-service
          image: busybox:1.36
          command:
            - sh
            - -c
            - "echo Application started; exit 1"
```

The pod may eventually show:

```text
0/1   CrashLoopBackOff
```

The assistant investigates using:

```bash
kubectl describe pod <pod-name> -n payments
```

```bash
kubectl logs <pod-name> -n payments --tail=200
```

```bash
kubectl logs <pod-name> -n payments --previous --tail=200
```

and:

```bash
kubectl get events -n payments --sort-by=.lastTimestamp
```

The assistant then distinguishes confirmed evidence from possible causes.

---

# Incident Analysis

The Analysis Node asks the LLM to produce:

```text
1. Incident Classification
2. Root Cause
3. Evidence
4. Recommended Fix
5. Verification Steps
6. Preventive Measures
```

The assistant is instructed to distinguish between:

## Confirmed Evidence

Facts directly obtained from Kubernetes or the runbook.

Example:

```text
Pod status: ImagePullBackOff
```

## Likely Cause

An inference based on the available evidence.

Example:

```text
The deployment likely references an unavailable container image.
```

## Unknown

Information that cannot be confirmed using the available evidence.

Example:

```text
The exact registry authentication failure cannot be confirmed
without the Kubernetes event output.
```

This approach reduces the chance of presenting an LLM assumption as a confirmed infrastructure fact.

---

# Local RAG

The current RAG implementation uses local runbooks stored in:

```text
runbooks/
```

Current runbooks include:

```text
database_timeout.txt
memory_leak.txt
service_restart.txt
image_startup_failure.md
crashloopbackoff.md
```

The current implementation uses lightweight keyword-based retrieval.

Example:

```text
Payment service is failing with ImagePullBackOff
```

can retrieve:

```text
image_startup_failure.md
```

The retrieved runbook is passed to the Analysis Node together with Kubernetes evidence.

## Current RAG Flow

```text
Incident Question
       |
       v
Keyword Matching
       |
       v
Local Runbooks
       |
       v
Top Matching Runbooks
       |
       v
LLM Analysis
```

No external vector database is required.

---

# Security and Safety

The assistant is designed as a **read-only diagnostic system**.

It does not automatically execute destructive Kubernetes operations such as:

```text
kubectl delete
kubectl apply
kubectl rollout restart
kubectl exec
```

The Kubernetes tools focus on collecting diagnostic information.

Recommended remediation commands should be reviewed and executed by an engineer.
<<<<<<< HEAD

The intended workflow is:

```text
Diagnose
   |
   v
Collect Evidence
   |
   v
Analyze
   |
   v
Recommend
   |
   v
Human Review
   |
   v
Remediate
```

rather than:

```text
Incident
   |
   v
AI
   |
   v
Automatic Production Change
```

---

# Environment Variables

The current Ollama implementation does not require an OpenAI API key.

Therefore:

```text
OPENAI_API_KEY
```

is not required.

The `.env` file should never contain credentials committed to Git.

The `.gitignore` contains:

```text
.env
.env.*
!.env.example
```

---

# Troubleshooting

## Ollama Connection Refused

If you see:

```text
Connection refused
```

verify that Ollama is running on Windows:

```powershell
ollama list
```

Start Ollama with:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
ollama serve
```

From WSL:

```bash
curl http://172.20.0.1:11434/api/tags
```

---

## LangChain Hangs While Waiting for the Model

If the traceback ends around:

```text
langchain_ollama
httpx
_sock.recv
```

the request has reached Ollama and is waiting for model output.

Try the smaller model:

```python
model="llama3.2:latest"
```

instead of:

```python
model="qwen3:8b"
```

Test:

```bash
python -c "from langchain_ollama import ChatOllama; llm=ChatOllama(model='llama3.2:latest', base_url='http://172.20.0.1:11434'); print(llm.invoke('What is Kubernetes?').content)"
```

---

## kubectl Not Found

If you see:

```text
kubectl is not installed or is not available in PATH
```

verify:

```bash
kubectl version --client
```

---

## Kubernetes Cluster Not Available

Test:

```bash
kubectl get nodes
```

If this fails, configure a Kubernetes cluster/context before running incident diagnostics.

---

# Future Improvements

Possible future enhancements include:

* Embedding-based RAG
* Chroma / FAISS / PGVector
* Azure AKS integration
* AWS EKS integration
* Prometheus metrics
* Grafana dashboards
* GitHub deployment history
* Azure DevOps deployment history
* Slack / Microsoft Teams incident notifications
* LangSmith tracing and evaluation
* Human approval workflows
* Automated incident ticket generation
* Incident timeline generation
* Multi-agent incident investigation
* Automated runbook recommendations
* LLM tool calling for Kubernetes diagnostics
* Production observability integration

---

# Project Goal

The long-term goal is to build a DevOps incident investigation assistant that connects:

```text
                 +-------------------+
                 | Incident Question |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |     LangGraph     |
                 +---------+---------+
                           |
              +------------+------------+
              |            |            |
              v            v            v
          Runbooks     Kubernetes   Observability
                         Evidence       Data
              |            |            |
              +------------+------------+
                           |
                           v
                 +-------------------+
                 |     Local LLM     |
                 |      Ollama       |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Incident Report   |
                 +-------------------+
```

The system is designed to help DevOps engineers investigate incidents faster while keeping production infrastructure changes under human control.
=======

The intended workflow is:

```text
Diagnose
   |
   v
Collect Evidence
   |
   v
Analyze
   |
   v
Recommend
   |
   v
Human Review
   |
   v
Remediate
```

rather than:

```text
Incident
   |
   v
AI
   |
   v
Automatic Production Change
```

---

# Environment Variables

The current Ollama implementation does not require an OpenAI API key.

Therefore:

```text
OPENAI_API_KEY
```

is not required.

The `.env` file should never contain credentials committed to Git.

The `.gitignore` contains:

```text
.env
.env.*
!.env.example
```

---

# Troubleshooting

## Ollama Connection Refused

If you see:

```text
Connection refused
```

verify that Ollama is running on Windows:

```powershell
ollama list
```

Start Ollama with:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
ollama serve
```

From WSL:

```bash
curl http://172.20.0.1:11434/api/tags
```

---

## LangChain Hangs While Waiting for the Model

If the traceback ends around:

```text
langchain_ollama
httpx
_sock.recv
```

the request has reached Ollama and is waiting for model output.

Try the smaller model:

```python
model="llama3.2:latest"
```

instead of:

```python
model="qwen3:8b"
```

Test:

```bash
python -c "from langchain_ollama import ChatOllama; llm=ChatOllama(model='llama3.2:latest', base_url='http://172.20.0.1:11434'); print(llm.invoke('What is Kubernetes?').content)"
```

---

## kubectl Not Found

If you see:

```text
kubectl is not installed or is not available in PATH
```

verify:

```bash
kubectl version --client
```

---

## Kubernetes Cluster Not Available

Test:

```bash
kubectl get nodes
```

If this fails, configure a Kubernetes cluster/context before running incident diagnostics.

---

# Future Improvements

Possible future enhancements include:

* Embedding-based RAG
* Chroma / FAISS / PGVector
* Azure AKS integration
* AWS EKS integration
* Prometheus metrics
* Grafana dashboards
* GitHub deployment history
* Azure DevOps deployment history
* Slack / Microsoft Teams incident notifications
* LangSmith tracing and evaluation
* Human approval workflows
* Automated incident ticket generation
* Incident timeline generation
* Multi-agent incident investigation
* Automated runbook recommendations
* LLM tool calling for Kubernetes diagnostics
* Production observability integration

---

# Project Goal

The long-term goal is to build a DevOps incident investigation assistant that connects:

```text
                 +-------------------+
                 | Incident Question |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |     LangGraph     |
                 +---------+---------+
                           |
              +------------+------------+
              |            |            |
              v            v            v
          Runbooks     Kubernetes   Observability
                         Evidence       Data
              |            |            |
              +------------+------------+
                           |
                           v
                 +-------------------+
                 |     Local LLM     |
                 |      Ollama       |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Incident Report   |
                 +-------------------+
```

The system is designed to help DevOps engineers investigate incidents faster while keeping production infrastructure changes under human control.

>>>>>>> 27fb2a5 (used ollma instead openai key)
