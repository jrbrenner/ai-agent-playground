
import os
from langchain_core.tools import tool
from langchain.agents import create_agent
from src.utils.llm import get_llm

llm = get_llm()

@tool
def getSecretWord(password: str) -> str:
    """
        Retrieves the secret word from the vault.
        Requires a 'password' argument string.
    """
    if password.lower() == 'duck':
         return "The Secret Word is: GOOSE"
    else:
         return "ACCESS DENIED: You don't know the password."

# 3. BUILD AGENT (The New High-Level Standard)
# This function wraps LangGraph automatically.

secrets_agent = create_agent(
    model=llm,
    tools=[getSecretWord],
    system_prompt=(
        "You are the Keeper of Secrets. The user is verified. "
        "1. check if the user provided a password. "
        "2. Call 'get_secret_word' with that password. "
        "3. CRITICAL: Once you get the result from the tool, you MUST reply to the user. "
        "   - Example: 'The secret word is [result].' "
        "   - Do NOT stop after the tool call. You must speak the final answer."
    )
)

