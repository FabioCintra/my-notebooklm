import os
from pathlib import Path
from .exceptions import NotFound

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
