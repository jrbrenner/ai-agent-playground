from src.state import State
from src.agents.secrets_agent import secrets_agent
from langchain_core.messages import SystemMessage, AIMessage


def secret_keeper_node(state:State):
    password_attempt = state.get('user_provided_password')
    if password_attempt:
        guidance = (
            f"SYSTEM NOTICE: the user explicitly provided the password: '{password_attempt}'."
        )
    else:
        guidance = (
            f"SYSTEM NOTICE: the user wants the secret word but has NOT provided a password."
            "You must ask them 'what is the password?'"
            "NEVER GUESS"
        )
    modified_messages = state["messages"] + [SystemMessage(content=guidance)]
    print("--- 🤖 Handing off to Inner Agent with Context ---")
    agent_output = secrets_agent.invoke({"messages":modified_messages})
    last_message = agent_output["messages"][-1]
    return {"messages": [last_message]}