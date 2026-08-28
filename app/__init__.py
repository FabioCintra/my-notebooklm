import os
from pathlib import Path
from .exceptions import NotFound
from .utils import get_path_folder
path_documents_temp = Path(__file__).resolve()

#path_state_db = get_path_folder("storage", "state_db")

__all__ = [
    'get_path_folder'
]