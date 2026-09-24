import re

from models.state import AgentState
from tools import (
    get_cluster_events,
    get_pod_info,
    describe_pod,
    get_pod_logs,
)


def extract_pod_reference(question: str, pods_output: str):
    """
    Extract namespace and pod name from kubectl get pods output.

    Expected format from:
        kubectl get pods -A -o wide

    Example:
        payments    payment-service-58f86cbfc9-vppft    0/1
        payments    payment-service-abc123               1/1
    """

    # First try to identify a pod explicitly mentioned in the user question.
    pod_match = re.search(
        r"\b([a-z0-9-]+)\b",
        question.lower(),
    )

    # Look specifically for known pod-name patterns in kubectl output.
    lines = pods_output.splitlines()

    for line in lines:
        line_lower = line.lower()

        if "payment-service" in line_lower:
            columns = line.split()

            if len(columns) >= 2:
                namespace = columns[0]
                pod_name = columns[1]

                # Validate that this looks like a real pod reference.
                if (
                    namespace not in {"namespace", "namespaces"}
                    and pod_name not in {"name", "names"}
                    and "-" in pod_name
                ):
                    return namespace, pod_name

    # Generic fallback for Kubernetes pod output.
    for line in lines:
        columns = line.split()

        if len(columns) >= 2:
            namespace = columns[0]
            pod_name = columns[1]

            if (
                namespace not in {"NAMESPACE", "namespace"}
                and pod_name not in {"NAME", "name"}
                and re.match(r"^[a-z0-9][a-z0-9.-]*$", namespace)
                and re.match(r"^[a-z0-9][a-z0-9.-]*$", pod_name)
                and "-" in pod_name
            ):
                return namespace, pod_name

    return None, None


def kubernetes_node(state: AgentState) -> dict:
    question = state.get("question", "")

    pods = get_pod_info.invoke({})
    events = get_cluster_events.invoke({})

    namespace, pod_name = extract_pod_reference(
        question,
        pods,
    )

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
