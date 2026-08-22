import os
from pathlib import Path
from .exceptions import NotFound

def get_path_folder(origin_path: Path, parent_folder_name: str, new_folder_name: str) -> str:
    path_documents_temp = origin_path

    folder_name = None
    path = None

    for father in path_documents_temp.parents:
        if father.name == parent_folder_name:
            folder_name = father
            break

    if folder_name:
        path = folder_name / new_folder_name
        os.makedirs(path, exist_ok=True)
        return path
    else:
        raise NotFound("Folder app not found!")
