import os
import base64
import tempfile
from pathlib import Path
from .exceptions import NotFound

from backend.app.schemas.notebook_schemas.DocumentInput import DocumentInput

def get_path_folder(
    origin_path: Path,
    parent_folder_name: str,
    *parts: str,
) -> str:
    origin_path = origin_path.resolve()

    current = origin_path.parent if origin_path.is_file() else origin_path

    for folder in [current, *current.parents]:
        if folder.name == parent_folder_name:
            path = folder.joinpath(*parts)
            os.makedirs(path, exist_ok=True)
            return path
        
    raise NotFound(
        f"Pasta '{parent_folder_name}' não encontrada."
    )

PATH_TEMP = get_path_folder(Path(__file__).resolve(), "app", "temp")

def load_pdf(document: DocumentInput, name_notebook: str):

    pdf_base64 = document.base64
    pdf_bytes = base64.b64decode(pdf_base64)
    
    temp_file = tempfile.NamedTemporaryFile(
        prefix=name_notebook,
        suffix=".pdf",
        delete=False,
        dir=PATH_TEMP
    )

    temp_file.write(pdf_bytes)
    temp_file.close()

def delete_file_temp():
    
    if PATH_TEMP.is_dir():
        for item in PATH_TEMP.iterdir():
            if item.is_file():
                item.unlink()