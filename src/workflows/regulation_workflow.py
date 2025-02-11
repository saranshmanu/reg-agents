from typing import TypedDict
from langgraph.graph import StateGraph, Graph
from ..agents import RegulationAgent, FlintFormatterAgent, ActorIdentificationAgent


class RegulationState(TypedDict):
    """State for regulation processing pipeline"""

    original_question: str
    regulation_text: str | None
    actor_analysis: str | None
    flint_format: str | None
    final_response: str | None
    error: str | None


def create_regulation_graph() -> Graph:
    """Creates a state graph for regulation processing"""

    # Initialize agents
    regulation_agent = RegulationAgent()
    actor_agent = ActorIdentificationAgent()
    flint_agent = FlintFormatterAgent()

    # Define state transformations
    def extract_regulation(state: RegulationState) -> RegulationState:
        try:
            regulation = regulation_agent.analyze_regulation(state["original_question"])
            state["regulation_text"] = regulation
            return state
        except Exception as e:
            state["error"] = f"Regulation extraction failed: {str(e)}"
            return state

    def identify_actors(state: RegulationState) -> RegulationState:
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
        state["error"] = "Could not find actors for the regulations. Cannot proceed with the request."
        return state

    def format_flint(state: RegulationState) -> RegulationState:
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
        """Determines if the regulation is eligible for FLINT formatting based on actor validation"""
        if state["actor_analysis"] != "Yes":
            return "no_actors"
        return "format"

    # Create state graph
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
