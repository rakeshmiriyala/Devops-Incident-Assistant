from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    runbook: str
    pods: str
    events: str
    describe: str
    logs: str
    response: str
