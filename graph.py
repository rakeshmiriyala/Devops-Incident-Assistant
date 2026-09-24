from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

from models.state import AgentState
from nodes.rag import rag_node
from nodes.k8s import kubernetes_node
from nodes.analysis import analysis_node


llm = ChatOllama(
    model="llama3.2:latest",
    base_url="http://172.20.0.1:11434",
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
