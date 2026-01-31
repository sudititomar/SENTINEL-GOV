from typing import TypedDict, Dict, Any

from langgraph.graph import StateGraph

from backend.agents.planner import run_planner_agent
from backend.agents.milestone_verifier import verify_milestone


# -------------------------
# ✅ CORRECT LANGGRAPH STATE
# -------------------------
# backend/agents/executer.py

def calculate_progress(verified_segments: int, total_segments: int) -> float:
    return round((verified_segments / total_segments) * 100, 2)

class ProjectState(TypedDict, total=False):
    # Inputs
    contract_text: str
    verified_segments: int

    # Intermediate
    contract_data: Dict[str, Any]
    progress_percent: float
    quality_verified: bool

    # Output
    verification_result: Dict[str, Any]


graph = StateGraph(ProjectState)


# -------------------------
# PLANNER NODE
# -------------------------
def planner_node(state: ProjectState) -> ProjectState:
    state["contract_data"] = run_planner_agent(state["contract_text"])
    return state


# -------------------------
# EXECUTOR NODE
# -------------------------
def executor_node(state: ProjectState) -> ProjectState:
    contract_data = state["contract_data"]

    total_segments = contract_data["total_segments"]
    verified_segments = state.get("verified_segments", 0)

    state["progress_percent"] = round(
        (verified_segments / total_segments) * 100, 2
    )

    return state


# -------------------------
# QUALITY NODE
# -------------------------
def quality_node(state: ProjectState) -> ProjectState:
    # Prototype default; later from image + lab agents
    state["quality_verified"] = state.get("quality_verified", True)
    return state


# -------------------------
# VERIFIER NODE (FINAL)
# -------------------------
def verifier_node(state: ProjectState) -> ProjectState:
    milestone = state["contract_data"]["milestones"][0]

    state["verification_result"] = verify_milestone(
        contract_milestone=milestone,
        actual_progress_percent=state["progress_percent"],
        quality_verified=state["quality_verified"]
    )

    return state


# -------------------------
# GRAPH WIRING
# -------------------------
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("quality", quality_node)
graph.add_node("verifier", verifier_node)

graph.set_entry_point("planner")

graph.add_edge("planner", "executor")
graph.add_edge("executor", "quality")
graph.add_edge("quality", "verifier")

workflow = graph.compile()
