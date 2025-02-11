"""
General question processing workflow that handles non-regulation questions
through a simplified analysis pipeline.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, Graph
from ..agents import GeneralAgent

class GeneralState(TypedDict):
    """
    State management for general questions:
    - original_question: Input question from user
    - analysis: Processed answer to question
    - final_response: Formatted response or error
    - error: Any processing errors
    """
    original_question: str
    analysis: str | None
    final_response: str | None
    error: str | None

def create_general_graph() -> Graph:
    """
    Creates a simple workflow for non-regulation questions:
    1. Analyzes and answers the question
    2. Prepares formatted response
    """
    
    # Initialize agent
    general_agent = GeneralAgent()
    
    def analyze_question(state: GeneralState) -> GeneralState:
        """Processes general questions to generate appropriate response"""
        try:
            analysis = general_agent.answer(state["original_question"])
            state["analysis"] = analysis
            return state
        except Exception as e:
            state["error"] = f"General analysis failed: {str(e)}"
            return state

    def prepare_response(state: GeneralState) -> GeneralState:
        """Formats the analysis result or error into final response format"""
        if state.get("error"):
            state["final_response"] = {"response": state["error"]}
            return state
            
        state["final_response"] = {
            "response": state["analysis"]
        }
        return state

    # Build simple linear workflow for general questions
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
