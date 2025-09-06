from agents.decision_agent import DecisionAgent
from agents.data_processing_agent import DataProcessingAgent
from agents.prediction_agent import PredictionAgent
from agents.optimization_agent import OptimizerAgent
from agents.action_agent import ActionAutomationAgent
from langgraph.graph import StateGraph
from typing import Dict, Any

# Define system state (shared across agents)
class MaintenanceState(dict):
    data: Dict[str, Any]
    predictions: Dict[str, Any]
    decision: Dict[str, Any]
    optimization: Dict[str, Any] 
    execution: Dict[str, Any] 
    supervisor_approval: str
    action: Dict[str, Any]

# Node wrapper
def data_processing_node(state: MaintenanceState) -> MaintenanceState:
    agent = DataProcessingAgent()
    output = agent.process()
    state["data"] = output
    return state

def prediction_node(state: MaintenanceState) -> MaintenanceState:
    agent = PredictionAgent()
    output = agent.analyze(state["data"])
    state["predictions"] = output
    return state

def decision_node(state: MaintenanceState) -> MaintenanceState:
    agent = DecisionAgent()
    predictions = state.get("predictions", {})
    print("Decision node input:", predictions)  

    output = agent.decide(predictions)

    decision_dict = {}
    if hasattr(output, "content"):
        decision_dict["decision"] = output.content
    elif isinstance(output, dict):
        decision_dict["decision"] = output.get("content", str(output))
        decision_dict["manual_context"] = output.get("manual_context", "")
    else:
        decision_dict["decision"] = str(output)
        decision_dict["manual_context"] = ""

    print("Decision node output:", decision_dict)  
    state["decision"] = decision_dict
    return state

def optimizer_node(state: MaintenanceState) -> MaintenanceState:
    agent = OptimizerAgent()
    decision = state.get("decision", {})
    print("Optimizer node input:", decision)

    output = agent.analyze_and_execute(decision)

    optimization_dict = {}
    if isinstance(output, dict):
        # store everything (structured + content)
        optimization_dict.update(output)
        if "content" in output:
            optimization_dict["optimization"] = output["content"]
    elif hasattr(output, "content"):
        optimization_dict["optimization"] = output.content
    else:
        optimization_dict["optimization"] = str(output)

    print("Optimizer node output:", optimization_dict)
    state["optimization"] = optimization_dict
    return state


def supervisor_node(state: MaintenanceState) -> MaintenanceState:
    print("\n--- Supervisor Review ---")
    optimization_result = state.get("optimization", {})
    report = optimization_result.get("optimization", "")

    print("Report:", report)

    approval = input("Supervisor, please approve (yes/no): ").strip().lower()
    state["supervisor_approval"] = approval
    return state

def action_node(state: MaintenanceState) -> MaintenanceState:
    agent = ActionAutomationAgent()

    optimized = state.get("optimization", {})
    approved = state.get("supervisor_approval", "no") == "yes"

    asset = optimized.get("asset", "Unknown-Asset")
    tasks = optimized.get("tasks", [])
    print('\n',tasks)
    parts = optimized.get("parts_report", [])
    print('\n',parts)
    technicians = optimized.get("available_techs", [])
    print('\n',technicians)
    supervisor_report = optimized.get("optimization", "")

    output = agent.execute(
        asset=asset,
        tasks=tasks,
        parts=parts,
        technicians=technicians,
        supervisor_report=supervisor_report,
        approved=approved
    )

    state["action"] = output
    return state

# Build the graph
def build_graph():
    workflow = StateGraph(MaintenanceState)
    
    workflow.add_node("data_processing", data_processing_node)
    workflow.add_node("prediction", prediction_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("optimizer", optimizer_node)
    workflow.add_node("supervisor", supervisor_node)   # ✅ add supervisor
    workflow.add_node("action", action_node)           # ✅ add action

    workflow.set_entry_point("data_processing")
    workflow.add_edge("data_processing", "prediction")
    workflow.add_edge("prediction", "decision")
    workflow.add_edge("decision", "optimizer")
    workflow.add_edge("optimizer", "supervisor")       # ✅ connect optimizer → supervisor
    workflow.add_edge("supervisor", "action")          # ✅ connect supervisor → action

    workflow.set_finish_point("action")                # ✅ finish at action
    return workflow
