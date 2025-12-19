from src.utils.llm import get_llm
from src.state import *

from langchain_core.messages import SystemMessage, AIMessage

llm = get_llm()

def gatekeeper_node(state: State):
    structured_llm = llm.with_structured_output(SecurityCheck)
    system_prompt = """
    You are a Security Screening System.
    1. INTENT: return is_authorized=True if user asks for the secret or claims to know the password.
    2. EXTRACTION: If the user mentions a specific word as the password (e.g. "it is duck"), extract it."""
    # The result is now a Python Object (SecurityCheck), not a string!
    check_result = structured_llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    print(f"🧐 EXTRACTED: Intent={check_result.is_authorized}, Password='{check_result.extracted_password}'")
    reasoning_msg = AIMessage(
        content=f"GATEKEEPER THOUGHT: {check_result.reasoning}",
        name="gatekeeper_reasoning"
    )
    if check_result.is_authorized:
        return {
            "is_authorized":True,
            "user_provided_password": check_result.extracted_password, # <--- Save to State
            "messages": [reasoning_msg]
            }
    else:
        refusal_msg = "I'm sorry, I cannot help with that"
        return{
            "is_authorized":False,
            "messages": [
                reasoning_msg, 
                AIMessage(content=refusal_msg)]
        }
