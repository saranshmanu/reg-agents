from typing import Dict, TypedDict
from langgraph.graph import Graph
from src.agents import (
    RouterAgent,
    GeneralAgent,
    RegulationAgent,
)


class State(TypedDict):
    """
    State object for managing conversation flow
    messages: List of conversation messages
    current_response: Current response being generated
    question_type: Classification of the current question
    analysis_result: Final analysis result from agents
    """
    messages: list[str]
    current_response: str
    question_type: Dict[str, str]
    analysis_result: str


# Initialize agent instances for different tasks
router = RouterAgent()        # Handles question classification
general_agent = GeneralAgent()    # Handles general queries
regulation_agent = RegulationAgent()  # Handles regulation-specific queries


def route_question(state: State) -> State:
    """
    Routes the question to appropriate agent based on classification
    Args:
        state: Current conversation state
    Returns:
        Updated state with question classification
    """
    question = state["messages"][-1]
    classification = router.classify_question(question)
    state["question_type"] = classification
    return state


def analyze_request(state: State) -> State:
    """
    Analyzes the request using appropriate specialized agent
    Args:
        state: Current conversation state containing question type
    Returns:
        Updated state with analysis results
    """
    question_type = state["question_type"]["type"]
    question = state["messages"][-1]
    
    if question_type == "REGULATION_QUESTION":
        analysis = regulation_agent.analyze_regulation(question)
    else:
        analysis = general_agent.answer(question)
    
    state["current_response"] = {
        "classification": question_type,
        "analysis": analysis
    }
    
    return state


def format_response(state: State) -> str:
    """Format the final response to be returned"""
    return state["current_response"]


def build_graph() -> Graph:
    """
    Builds the conversation workflow graph
    The graph follows this pattern:
    route -> analyze -> format
    Returns:
        Compiled workflow graph
    """
    workflow = Graph()

    workflow.add_node("route", route_question)
    workflow.add_node("analyze", analyze_request)
    workflow.add_node("format", format_response)

    # Configure workflow
    workflow.set_entry_point("route")
    workflow.add_edge("route", "analyze")
    workflow.add_edge("analyze", "format")
    workflow.set_finish_point("format")

    return workflow.compile()


def process_message_flow(message: str) -> str:
    """
    Main entry point for processing messages
    Args:
        message: User input message
    Returns:
        Processed response from appropriate agent
    """
    graph = build_graph()
    state = {
        "messages": [message],
        "current_response": "",
        "question_type": {},
        "analysis_result": "",
    }
    result = graph.invoke(state)
    return result
