import uuid

from app.schemas.notebook_schemas.DocumentInput import DocumentInput
from app.schemas.notebook_schemas.NotebookResponse import NotebookResponse
from app.rag import save_documents
from app import repository
from app import load_pdf

def create(documents: list[DocumentInput], name_notebook: str) -> NotebookResponse:
    for doc in documents:
        load_pdf(doc, name_notebook)

    thread_id: str = str(uuid.uuid4())
    save_documents(thread_id)

    notebook: NotebookResponse = NotebookResponse(
                name_notebook=name_notebook,
                thread_id=thread_id
            )
    repository.save(notebook)
    return notebook

def get_all() -> list[NotebookResponse]:
    return repository.get_all()

async def delete_notebook(thread_id: str):
    await repository.delete(thread_id)
