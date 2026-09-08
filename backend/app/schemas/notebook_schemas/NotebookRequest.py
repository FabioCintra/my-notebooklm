from pydantic import BaseModel
from backend.app.schemas.notebook_schemas.DocumentInput import DocumentInput

class NotebookRequest(BaseModel):
    name_notebook: str
    documents: list[DocumentInput]