import subprocess
from langchain.tools import tool


def run_kubectl(args: list[str], timeout: int = 30) -> str:
    """Run a read-only kubectl command and return stdout/stderr."""
    command = ["kubectl", *args]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return (
            "kubectl is not installed or is not available in PATH. "
            "Install kubectl and configure kubeconfig."
        )
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds: {' '.join(command)}"

    output = result.stdout.strip()
    error = result.stderr.strip()

    if result.returncode != 0:
        return (
            f"Command failed with exit code {result.returncode}.\n"
            f"STDOUT:\n{output}\n"
            f"STDERR:\n{error}"
        )

    return output or "(command returned no output)"


@tool
def get_pod_info() -> str:
    """Get all Kubernetes pods with namespace, status, IP and node."""
    return run_kubectl(["get", "pods", "-A", "-o", "wide"])


@tool
def get_cluster_events() -> str:
    """Get Kubernetes cluster events sorted by the most recent timestamp."""
    return run_kubectl(
        ["get", "events", "-A", "--sort-by=.lastTimestamp"]
    )


@tool
def describe_pod(pod_name: str, namespace: str) -> str:
    """Describe a specific Kubernetes pod."""
    if not pod_name or not namespace:
        return "Pod name and namespace are required."

    return run_kubectl(
        ["describe", "pod", pod_name, "-n", namespace]
    )


@tool
def get_pod_logs(
    pod_name: str,
    namespace: str,
    previous: bool = False,
) -> str:
    """Get recent logs from a Kubernetes pod."""
    if not pod_name or not namespace:
        return "Pod name and namespace are required."

    args = [
        "logs",
        pod_name,
        "-n",
        namespace,
        "--tail=200",
    ]

    if previous:
        args.insert(3, "--previous")

    return run_kubectl(args)
