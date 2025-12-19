from langchain_core.tools import tool

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