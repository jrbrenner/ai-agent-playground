from langgraph.graph import StateGraph, START, END
from src.state import State
from src.nodes.gatekeeper import gatekeeper_node
from src.nodes.secretkeeper import secret_keeper_node
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, Literal, Optional


def route_decision(state: State) -> Literal["secret_keeper", "__end__"]:
    last_message = state['messages'][-1]
    content = last_message.content.strip().upper()
    if state.get("is_authorized") == True:
        return "secret_keeper"
    else:
        return "__end__"

# Initialize the graph with our State schema
graph_builder = StateGraph(State)

# Add our node
graph_builder.add_node("gatekeeper", gatekeeper_node)
graph_builder.add_node("secret_keeper", secret_keeper_node)

# Add edges (Flow logic)
graph_builder.add_edge(START, "gatekeeper")

graph_builder.add_conditional_edges(
    "gatekeeper", 
    route_decision, 
    {
        "secret_keeper": "secret_keeper", 
        "__end__": END
    }
)

# Compile the graph (This creates the runnable app)
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)