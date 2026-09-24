from models.state import AgentState
from knowledge_base import retrieve_runbook


def rag_node(state: AgentState) -> dict:
    question = state.get("question", "")

    return {
        "runbook": retrieve_runbook(question)
    }
