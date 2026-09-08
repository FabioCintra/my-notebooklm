from pydantic import BaseModel

class AnswerRequest(BaseModel):
    thread_id: str
    prompt: str
    
class AnswerResponse(BaseModel):
    answer: str


