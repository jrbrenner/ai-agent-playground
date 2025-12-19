#THE PROTOCOL: Defines State & Pydantic Schemas


from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from typing import Annotated, Literal, Optional
from langgraph.graph.message import add_messages


class State(TypedDict):
    # 'add_messages' ensures new messages are appended to history
    messages: Annotated[list, add_messages]
    is_authorized: Optional[bool]
    user_provided_password: Optional[str]


class SecurityCheck(BaseModel):
    is_authorized: bool = Field(description = "true is the user wants the secret word, False otherwise")
    extracted_password: Optional[str] = Field(description = "the specific password provided by the user. If none, return None")
    reasoning: str = Field (description = "brief description of why the user was accepted or rejected")