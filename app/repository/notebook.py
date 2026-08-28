import json
from . import *
from app.schemas.notebook_schemas.NotebookResponse import NotebookResponse as Notebook

def read_file() -> list[Notebook]:
    with open(notebook_bd_path, "r", encoding="utf-8") as file:
        data = json.load(file)

        if not data:
            return []

        notebooks: list[Notebook] = [
            Notebook(
                notebook_name=d["notebook_name"],
                thread_id=d["thread_id"]
            ) for d in data
        ]

        return notebooks
def write_file(notebooks: list[Notebook]):
    list_for_save = [n.__dict__ for n in notebooks]
    with open(notebook_bd_path, "w", encoding="utf-8") as file:
        json.dump(list_for_save, file, indent=4, ensure_ascii=False)

def save(new_notebook: Notebook):
    notebooks: list[Notebook] = read_file()
    notebooks.append(new_notebook)
    write_file(notebooks)

