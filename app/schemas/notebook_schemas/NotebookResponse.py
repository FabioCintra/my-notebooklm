from pydantic import BaseModel

class NotebookResponse(BaseModel):
    name_notebook: str
    thread_id: str