from pyarrow.lib import UUID
from pydantic import BaseModel

class AnswerRequest(BaseModel):
    thread_id: UUID
    prompt: str
    
class AnswerResponse(BaseModel):
    answer: str


