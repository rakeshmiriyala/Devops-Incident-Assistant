# 🚨 DevOps Incident Assistant

> An AI-powered Kubernetes incident investigation assistant built with **LangGraph, LangChain, Ollama, and Kubernetes**.

DevOps Incident Assistant combines **local runbooks**, **live Kubernetes diagnostics**, and a **local LLM** to investigate infrastructure incidents and generate structured incident analysis.

---

## ✨ Features

* 🔎 **Runbook Retrieval** — Finds relevant troubleshooting knowledge from local runbooks.
* ☸️ **Kubernetes Diagnostics** — Collects pod, event, description, and log information.
* 🧠 **Local LLM Analysis** — Uses Ollama to analyze incident evidence.
* 📋 **Structured Reports** — Generates classification, root cause, evidence, fixes, and verification steps.
* 🛡️ **Read-Only Diagnostics** — Does not automatically modify Kubernetes resources.
* 🔐 **No OpenAI API Key Required** — Runs using local Ollama models.

---

## 🏗️ Architecture

```text
                         User
                          |
                          v
                  Incident Question
                          |
                          v
                     LangGraph
                          |
             +------------+------------+
             |            |            |
             v            v            v
          RAG Node   Kubernetes Node  Analysis Node
             |            |            |
             v            v            v
        Runbooks       kubectl       Ollama LLM
             |            |            |
             +------------+------------+
                          |
                          v
                  Incident Analysis
```

### Investigation Flow

```text
Incident Question
       |
       v
Retrieve Runbook
       |
       v
Collect Kubernetes Evidence
       |
       +--> Pods
       +--> Events
       +--> Describe Pod
       +--> Logs
       |
       v
LLM Analysis
       |
       v
Incident Report
       |
       +--> Classification
       +--> Root Cause
       +--> Evidence
       +--> Recommended Fix
       +--> Verification
       +--> Prevention
```

---

## 🛠️ Tech Stack

| Component         | Technology                    |
| ----------------- | ----------------------------- |
| Language          | Python                        |
| Agent Framework   | LangGraph                     |
| LLM Framework     | LangChain                     |
| Local LLM Runtime | Ollama                        |
| Models            | `llama3.2`, `qwen3:8b`        |
| Kubernetes        | kubectl                       |
| RAG               | Local keyword-based retrieval |
| Environment       | Linux / WSL / Windows         |

---

## 📁 Project Structure

```text
Devops-Incident-Assistant/
│
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

# 🚀 Getting Started

## Prerequisites

Make sure you have:

* Python 3.10+
* Git
* Kubernetes
* `kubectl`
* Ollama
* A running/configured Kubernetes cluster

---

## 1. Clone the Repository

```bash
git clone https://github.com/rakeshmiriyala/devops-incident-assistant.git

cd devops-incident-assistant
```

---

## 2. Create a Virtual Environment

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

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🧠 Ollama Setup

This project uses **Ollama** for local LLM inference.

No OpenAI API key is required.

### Pull a Model

```bash
ollama pull llama3.2
```

Or:

```bash
ollama pull qwen3:8b
```

Verify:

```bash
ollama list
```

Example:

```text
NAME
llama3.2:latest
qwen3:8b
```

---

# ☸️ Kubernetes Setup

Verify `kubectl`:

```bash
kubectl version --client
```

Check the current context:

```bash
kubectl config current-context
```

Test cluster connectivity:

```bash
kubectl get pods -A
```

The assistant requires access to a Kubernetes cluster so it can collect diagnostic information.

---

# ▶️ Run the Application

Start the application:

```bash
python main.py
```

You will be prompted with:

```text
Ask Incident Question:
```

Example:

```text
Payment service is failing after deployment. Investigate the incident.
```

The assistant will:

```text
1. Receive the incident
2. Search relevant runbooks
3. Collect Kubernetes information
4. Analyze the collected evidence
5. Generate an incident report
```

---

# 🔍 Kubernetes Diagnostics

The assistant uses read-only Kubernetes commands such as:

```bash
kubectl get pods -A -o wide
```

```bash
kubectl get events -A --sort-by=.lastTimestamp
```

```bash
kubectl describe pod <pod-name> -n <namespace>
```

```bash
kubectl logs <pod-name> -n <namespace> --tail=200
```

```bash
kubectl logs <pod-name> -n <namespace> --previous --tail=200
```

These commands help collect the evidence required for incident investigation.

---

# 📚 RAG

The project currently uses a lightweight local RAG implementation.

Runbooks are stored under:

```text
runbooks/
```

Example runbooks:

```text
database_timeout.txt
memory_leak.txt
service_restart.txt
image_startup_failure.md
crashloopbackoff.md
```

### RAG Flow

```text
Incident Question
       |
       v
Keyword Retrieval
       |
       v
Relevant Runbook
       |
       v
Kubernetes Evidence
       |
       v
LLM Analysis
```

The current implementation does **not require a vector database**.

Future versions can use:

```text
FAISS
Chroma
PGVector
```

for embedding-based retrieval.

---

# 🧠 Incident Analysis

The Analysis Node generates a structured incident report containing:

```text
1. Incident Classification
2. Root Cause
3. Evidence
4. Recommended Fix
5. Verification Steps
6. Preventive Measures
```

The assistant attempts to distinguish between:

### ✅ Confirmed Evidence

Information directly obtained from Kubernetes or runbooks.

Example:

```text
Pod Status: ImagePullBackOff
```

### ⚠️ Likely Cause

A conclusion inferred from the available evidence.

Example:

```text
The deployment may reference an unavailable container image.
```

### ❓ Unknown

Information that cannot be confirmed with the available evidence.

Example:

```text
The exact registry authentication problem cannot be confirmed
without additional Kubernetes event information.
```

This helps reduce the risk of treating an LLM assumption as a confirmed infrastructure fact.

---

# 🧪 Example Incident

Consider a deployment with an invalid image:

```yaml
image: nginx-does-not-exist:999
```

Kubernetes may report:

```text
ErrImagePull
ImagePullBackOff
```

The assistant collects:

```text
Pod Status
    +
Kubernetes Events
    +
Pod Description
    +
Container Logs
    +
Relevant Runbook
    |
    v
Local LLM
    |
    v
Incident Analysis
```

Example output:

```text
Incident Classification:
ImagePullBackOff

Root Cause:
The configured container image is unavailable or invalid.

Evidence:
- Pod is unable to start
- Kubernetes reports image pull failure
- Image reference is nginx-does-not-exist:999

Recommended Fix:
Verify the image repository and tag.

Verification:
Confirm the pod reaches Running state after correction.
```

> The LLM response can vary between runs. Production changes should always be reviewed by an engineer.

---

# 🔐 Safety

The project is designed as a **diagnostic assistant**, not an autonomous production remediation system.

It does not automatically execute destructive or state-changing commands such as:

```text
kubectl delete
kubectl apply
kubectl rollout restart
kubectl exec
```

The intended workflow is:

```text
       Incident
          |
          v
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

This keeps production changes under human control.

---

# 🖥️ Ollama + WSL

If Python runs inside WSL while Ollama runs on Windows, Ollama may need to be exposed to WSL.

Run in Windows PowerShell:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"

ollama serve
```

Find the WSL gateway:

```bash
ip route
```

Example:

```text
default via 172.20.0.1 dev eth0
```

Then configure the Ollama URL in the application:

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:latest",
    base_url="http://172.20.0.1:11434",
    temperature=0,
)
```

If Ollama and the application run in the same environment:

```text
http://localhost:11434
```

can generally be used.

---

# 🔧 Troubleshooting

## Ollama Connection Refused

Check Ollama:

```powershell
ollama list
```

Start it:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"

ollama serve
```

From WSL:

```bash
curl http://<WSL-GATEWAY>:11434/api/tags
```

---

## kubectl Not Found

Check:

```bash
kubectl version --client
```

Make sure `kubectl` is installed and available in your `PATH`.

---

## Kubernetes Connection Failed

Check:

```bash
kubectl config current-context
```

Then:

```bash
kubectl get nodes
```

Make sure the selected Kubernetes context is available.

---

# 📈 Future Improvements

Planned improvements include:

* 🔹 Embedding-based RAG
* 🔹 FAISS / Chroma / PGVector
* 🔹 Azure AKS integration
* 🔹 AWS EKS integration
* 🔹 Prometheus integration
* 🔹 Grafana observability
* 🔹 GitHub deployment history
* 🔹 Azure DevOps deployment history
* 🔹 LangSmith tracing
* 🔹 Slack / Microsoft Teams notifications
* 🔹 Incident ticket generation
* 🔹 Human approval workflows
* 🔹 Automated incident timelines
* 🔹 Multi-agent investigation
* 🔹 Production observability integration

---

# 🎯 Project Goal

The long-term goal is to connect DevOps incident investigation with AI-assisted reasoning:

```text
                 Incident
                    |
                    v
        +-----------------------+
        |       LangGraph       |
        +-----------+-----------+
                    |
          +---------+---------+
          |         |         |
          v         v         v
      Runbooks  Kubernetes  Observability
          |         |         |
          +---------+---------+
                    |
                    v
              Local LLM
                Ollama
                    |
                    v
          Incident Analysis
                    |
                    v
            Human Review
                    |
                    v
              Remediation
```

The goal is to help DevOps engineers **investigate incidents faster while keeping production changes under human control**.

---

# 👨‍💻 Author

**Rakesh Miriyala**

GitHub:
https://github.com/rakeshmiriyala

---
