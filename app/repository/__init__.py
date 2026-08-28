from pathlib import Path
from app import get_path_folder

notebook_bd_path_temp = Path(
    get_path_folder(
        Path(__file__).resolve(),
        "app",
        "storage",
        "repositories"
    )
)

path_temp = notebook_bd_path_temp / "notebook_bd.txt"
path_temp.write_text("[]", encoding="utf-8")

notebook_bd_path = str(path_temp)

from .notebook import save

__all__ = [
    "notebook_bd_path",
    "save"
]