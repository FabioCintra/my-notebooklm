import json
from pathlib import Path
from . import *
from app import get_path_folder
from app.schemas.notebook_schemas.NotebookResponse import NotebookResponse as Notebook
from . import messages as MessagesRepository, embeddings as EmbeddingsRepository

def check_exists_bd_file() -> str:
    notebook_bd_path= Path(
    get_path_folder(
        Path(__file__).resolve(),
        "app",
        "storage",
        "repositories"
    )
)
    path = notebook_bd_path / "notebook_bd.txt"
    if not path.is_file():
        path.write_text("[]", encoding="utf-8")

    return str(path)

def read_file() -> list[Notebook]:
    notebook_bd_path = check_exists_bd_file()
    
    with open(notebook_bd_path, "r", encoding="utf-8") as file:
        data = json.load(file)

        if not data:
            return []

        notebooks: list[Notebook] = [
            Notebook(
                name_notebook=d["name_notebook"],
                thread_id=d["thread_id"]
            ) for d in data
        ]

        return notebooks
def write_file(notebooks: list[Notebook]):
    notebook_bd_path = check_exists_bd_file()

    list_for_save = [n.__dict__ for n in notebooks]
    with open(notebook_bd_path, "w", encoding="utf-8") as file:
        json.dump(list_for_save, file, indent=4, ensure_ascii=False)

def save(new_notebook: Notebook):
    notebooks: list[Notebook] = read_file()
    notebooks.append(new_notebook)
    write_file(notebooks)

def get_all():
    return read_file()

async def delete(thread_id: str):
    notebooks: list[Notebook] = read_file()
    notebooks_updated: list[Notebook] = list(filter(lambda notebook: notebook.thread_id != thread_id, notebooks ))
    write_file(notebooks_updated)

    await MessagesRepository.delete_chat(thread_id)

    EmbeddingsRepository.delete_embeddings(thread_id)

