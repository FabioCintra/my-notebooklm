import os
from pathlib import Path
from .exceptions import NotFound
from .utils import get_path_folder, load_pdf, delete_file_temp
path_documents_temp = Path(__file__).resolve()


__all__ = [
    'get_path_folder',
    'load_pdf',
    'delete_file_temp'
]