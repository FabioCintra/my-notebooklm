from pydantic import BaseModel
from typing import Literal

class ChatResponse(BaseModel):
    identifier: Literal["Human", "AI"]
    message: str