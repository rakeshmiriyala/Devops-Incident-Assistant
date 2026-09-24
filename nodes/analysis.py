from models.state import AgentState


def analysis_node(state: AgentState, llm) -> dict:
    prompt = f"""
You are a Senior DevOps / Kubernetes Incident Engineer.

Analyze the incident using ONLY the supplied question, runbook and
Kubernetes evidence.

Important:
- Do not invent Kubernetes facts.
- Clearly separate observed evidence from inference.
- An incorrect image name usually causes ErrImagePull or ImagePullBackOff.
- CrashLoopBackOff means the container started and repeatedly exited.
- If the evidence is insufficient, say what additional command or evidence
  is required.
- Never recommend destructive Kubernetes commands automatically.
- Give commands as examples for an engineer to review and execute.

USER QUESTION:
{state.get("question", "")}

LOCAL RUNBOOK:
{state.get("runbook", "")}

KUBERNETES PODS:
{state.get("pods", "")}

KUBERNETES EVENTS:
{state.get("events", "")}

POD DESCRIPTION:
{state.get("describe", "")}

POD LOGS:
{state.get("logs", "")}

Return the incident analysis in this format:

1. Incident Classification
2. Root Cause
3. Evidence
4. Recommended Fix
5. Verification Steps
6. Preventive Measures

For the Root Cause and Evidence sections, distinguish confirmed facts
from likely causes.
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }
