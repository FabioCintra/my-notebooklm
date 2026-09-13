from fastapi import APIRouter,status
from app.schemas.notebook_schemas.NotebookRequest import NotebookRequest
from app.schemas.notebook_schemas.NotebookResponse import NotebookResponse
from app.schemas.notebook_schemas.DocumentInput import DocumentInput
from app.schemas.ChatResponse import ChatResponse
from app.services import notebook as NotebookService

router = APIRouter(
    prefix="/notebooks",
    tags=["Notebooks"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_notebook(request: NotebookRequest) -> NotebookResponse:
    name_notebook: str = request.name_notebook
    documents: list[DocumentInput] = request.documents
    
    notebook_saved = NotebookService.create(documents, name_notebook)
    return notebook_saved
    

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_notebooks():
    return NotebookService.get_all()

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notebook(thread_id: str):
    await NotebookService.delete_notebook(thread_id)

@router.get("/messages/{thread_id}", status_code=status.HTTP_200_OK)
async def notebook_messages(thread_id: str) -> list[ChatResponse]:
    messages: list[ChatResponse] = await NotebookService.messages_chat(thread_id)
    return messages
