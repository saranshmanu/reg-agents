from typing import TypedDict
from langgraph.graph import StateGraph, Graph
from ..agents import GeneralAgent

class GeneralState(TypedDict):
    """State for general question processing pipeline"""
    original_question: str
    analysis: str | None
    final_response: str | None
    error: str | None

def create_general_graph() -> Graph:
    """Creates a state graph for general question processing"""
    
    # Initialize agent
    general_agent = GeneralAgent()
    
    def analyze_question(state: GeneralState) -> GeneralState:
        try:
            analysis = general_agent.answer(state["original_question"])
            state["analysis"] = analysis
            return state
        except Exception as e:
            state["error"] = f"General analysis failed: {str(e)}"
            return state

    def prepare_response(state: GeneralState) -> GeneralState:
        if state.get("error"):
            state["final_response"] = state["error"]
            return state
            
        state["final_response"] = {
            "analysis": state["analysis"]
        }
        return state

    # Create state graph
    workflow = StateGraph(GeneralState)
    
    # Add nodes
    workflow.add_node("analyze", analyze_question)
    workflow.add_node("prepare", prepare_response)

    # Add edges
    workflow.add_edge("analyze", "prepare")

    # Set entry and exit
    workflow.set_entry_point("analyze")
    workflow.set_finish_point("prepare")

    return workflow.compile()
