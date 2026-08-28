from pyarrow.lib import UUID
import uuid

from app.schemas.notebook_schemas.DocumentInput import DocumentInput
from app.schemas.notebook_schemas.NotebookResponse import NotebookResponse
from app.rag import load_pdf, save_documents
from app.repository import save

def create(documents: list[DocumentInput], name_notebook: str) -> NotebookResponse:
    for doc in documents:
        load_pdf(doc)

    thread_id: str = str(uuid.uuid4())
    save_documents(thread_id)

    notebook: NotebookResponse = NotebookResponse(
                name_notebook=name_notebook,
                thread_id=thread_id
            )
    save(notebook)
    return notebook