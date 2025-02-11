from typing import TypedDict
from langgraph.graph import StateGraph, Graph
from ..agents import RegulationAgent, FlintFormatterAgent, ActorIdentificationAgent

"""
Regulation processing workflow that handles:
1. Regulation text extraction
2. Actor identification
3. FLINT formatting
4. Response preparation
"""

class RegulationState(TypedDict):
    """
    State management for regulation processing:
    - original_question: Input question from user
    - regulation_text: Extracted regulation content
    - actor_analysis: Result of actor identification ("Yes"/"No")
    - flint_format: Formatted regulation in FLINT
    - final_response: Processed response or error message
    - error: Any processing errors
    """
    original_question: str
    regulation_text: str | None
    actor_analysis: str | None
    flint_format: str | None
    final_response: str | None
    error: str | None


def create_regulation_graph() -> Graph:
    """
    Creates a workflow for processing regulation questions:
    1. Extracts relevant regulation text
    2. Identifies actors in the regulation
    3. If actors found, formats to FLINT
    4. Prepares final response with all components
    """
    
    # Initialize specialized agents for each processing step
    regulation_agent = RegulationAgent()
    actor_agent = ActorIdentificationAgent()
    flint_agent = FlintFormatterAgent()

    def extract_regulation(state: RegulationState) -> RegulationState:
        """Extracts relevant regulation text from the question"""
        try:
            regulation = regulation_agent.analyze_regulation(state["original_question"])
            state["regulation_text"] = regulation
            return state
        except Exception as e:
            state["error"] = f"Regulation extraction failed: {str(e)}"
            return state

    def identify_actors(state: RegulationState) -> RegulationState:
        """
        Analyzes regulation text to identify relevant actors
        Returns "Yes" if actors found, otherwise indicates no actors
        """
        if state.get("error"):
            return state
        try:
            actors = actor_agent.identify(state["regulation_text"])
            state["actor_analysis"] = actors
            return state
        except Exception as e:
            state["error"] = f"Actor identification failed: {str(e)}"
            return state

    def handle_no_actors(state: RegulationState) -> RegulationState:
        """Sets error state when no actors are identified in regulation"""
        state["error"] = "Could not find actors for the regulations. Cannot proceed with the request."
        return state

    def format_flint(state: RegulationState) -> RegulationState:
        """Converts regulation text to FLINT format if actors were identified"""
        if state.get("error"):
            return state
        try:
            flint = flint_agent.format(state["regulation_text"])
            state["flint_format"] = flint
            return state
        except Exception as e:
            state["error"] = f"Flint formatting failed: {str(e)}"
            return state

    def prepare_response(state: RegulationState) -> RegulationState:
        """
        Assembles final response including:
        - Original regulation text
        - Actor analysis results
        - FLINT formatted version (if applicable)
        - Any error messages
        """
        print("Preparing response", state["error"])
        if state.get("error"):
            state["final_response"] = {"response": state["error"]}
            return state

        state["final_response"] = {
            "regulation": state["regulation_text"],
            "actor_analysis": state["actor_analysis"],
            "response": state["flint_format"],
        }
        return state

    def determine_flint_eligibility(state: RegulationState | str) -> str:
        """
        Determines whether to proceed with FLINT formatting:
        - Returns "format" if actors were identified
        - Returns "no_actors" if no actors found
        """
        if state["actor_analysis"] != "Yes":
            return "no_actors"
        return "format"

    # Build workflow graph with conditional routing based on actor identification
    workflow = StateGraph(RegulationState)

    # Add nodes
    workflow.add_node("extract", extract_regulation)
    workflow.add_node("identify", identify_actors)
    workflow.add_node("format", format_flint)
    workflow.add_node("prepare", prepare_response)
    workflow.add_node("no_actors", handle_no_actors)

    # Add edges with routing function
    workflow.add_edge("extract", "identify")
    workflow.add_conditional_edges("identify", determine_flint_eligibility)
    workflow.add_edge("format", "prepare")
    workflow.add_edge("no_actors", "prepare")

    # Set entry and exit points
    workflow.set_entry_point("extract")
    workflow.set_finish_point("prepare")

    return workflow.compile()
