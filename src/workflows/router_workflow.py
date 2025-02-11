"""
Main router workflow that handles incoming questions and directs them to appropriate processors.
Determines if a question is regulation-related or general and routes accordingly.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, Graph
from ..agents import RouterAgent
from .regulation_workflow import create_regulation_graph
from .general_workflow import create_general_graph

class RouterState(TypedDict):
    """
    State management for the router pipeline
    - message: Original user question
    - question_type: Classification result determining question category
    - response: Final processed response from appropriate workflow
    - error: Any error messages during processing
    """
    message: str
    question_type: dict | None
    response: dict | None
    error: str | None

def create_router_graph() -> Graph:
    """
    Creates a workflow graph that:
    1. Classifies incoming questions
    2. Routes to appropriate processor (regulation or general)
    3. Returns processed response
    """
    
    # Initialize router agent
    router = RouterAgent()
    
    def classify_question(state: RouterState) -> RouterState:
        """Determines if the question is regulation-related or general"""
        try:
            classification = router.classify_question(state["message"])
            state["question_type"] = classification
            return state
        except Exception as e:
            state["error"] = f"Question classification failed: {str(e)}"
            return state

    def process_request(state: RouterState) -> RouterState:
        """
        Routes the question to appropriate processor based on classification:
        - REGULATION_QUESTION: Handled by regulation workflow
        - Other: Handled by general workflow
        """
        if state.get("error"):
            return state
            
        try:
            question_type = state["question_type"]["type"]
            
            if question_type == "REGULATION_QUESTION":
                workflow = create_regulation_graph()
                result = workflow.invoke({
                    "original_question": state["message"],
                    "regulation_text": None,
                    "actor_analysis": None,
                    "flint_format": None,
                    "final_response": None,
                    "error": None
                })
            else:
                workflow = create_general_graph()
                result = workflow.invoke({
                    "original_question": state["message"],
                    "analysis": None,
                    "final_response": None,
                    "error": None
                })
            
            state["response"] = {
                "classification": question_type,
                **result["final_response"]
            }
            return state
            
        except Exception as e:
            state["error"] = f"Request processing failed: {str(e)}"
            return state

    # Create state graph
    workflow = StateGraph(RouterState)
    
    # Add nodes
    workflow.add_node("classify", classify_question)
    workflow.add_node("process", process_request)

    # Add edges
    workflow.add_edge("classify", "process")

    # Set entry and exit
    workflow.set_entry_point("classify")
    workflow.set_finish_point("process")

    return workflow.compile()

