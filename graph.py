from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from models.state import AgentState
from nodes.rag import rag_node
from nodes.k8s import kubernetes_node
from nodes.analysis import analysis_node


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


def analysis_with_llm(state: AgentState):
    return analysis_node(state, llm)


graph = StateGraph(AgentState)

graph.add_node("rag", rag_node)
graph.add_node("k8s", kubernetes_node)
graph.add_node("analysis", analysis_with_llm)

graph.set_entry_point("rag")
graph.add_edge("rag", "k8s")
graph.add_edge("k8s", "analysis")
graph.add_edge("analysis", END)

app = graph.compile()
