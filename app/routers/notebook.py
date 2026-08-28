from fastapi import APIRouter,status
from app.schemas.notebook_schemas.NotebookRequest import NotebookRequest
from app.schemas.notebook_schemas.NotebookResponse import NotebookResponse
from app.schemas.notebook_schemas.DocumentInput import DocumentInput
from app.services.notebook import create

router = APIRouter(
    prefix="/notebooks",
    tags=["Notebooks"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_notebook(request: NotebookRequest) -> NotebookResponse:
    name_notebook: str = request.name_notebook
    documents: list[DocumentInput] = request.documents
    
    notebook_saved = create(documents, name_notebook)
    return notebook_saved
    

# @router.get("/", status_code=status.HTTP_200_OK)
# def get_all_notebooks():

# @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# def delete_notebook(thread_id: UUID):

