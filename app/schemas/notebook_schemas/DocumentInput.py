from pydantic import BaseModel

class DocumentInput(BaseModel):
    file_name: str
    mime_type: str
    base64: str
