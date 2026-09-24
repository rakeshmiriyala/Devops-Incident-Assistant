import re

from models.state import AgentState
from tools import (
    get_cluster_events,
    get_pod_info,
    describe_pod,
    get_pod_logs,
)


def extract_pod_reference(text: str):
    """Best-effort extraction of namespace/pod from common kubectl output."""
    patterns = [
        r"(?:pod|namespace/pod)\s+([a-z0-9-]+)/([a-z0-9.-]+)",
        r"\b([a-z0-9-]+)/([a-z0-9.-]+)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1), match.group(2)

    return None, None


def kubernetes_node(state: AgentState) -> dict:
    question = state.get("question", "")

    pods = get_pod_info.invoke({})
    events = get_cluster_events.invoke({})

    combined = f"{question}\n{pods}\n{events}"
    namespace, pod_name = extract_pod_reference(combined)

    describe = ""
    logs = ""

    if namespace and pod_name:
        describe = describe_pod.invoke(
            {
                "pod_name": pod_name,
                "namespace": namespace,
            }
        )

        logs = get_pod_logs.invoke(
            {
                "pod_name": pod_name,
                "namespace": namespace,
                "previous": False,
            }
        )

    return {
        "pods": pods[:12000],
        "events": events[-12000:],
        "describe": describe[:12000],
        "logs": logs[-12000:],
    }
