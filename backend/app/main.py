from fastapi import FastAPI
from backend.app.routers import notebook
from backend.app.routers import llm

app = FastAPI()

app.include_router(llm.router)
app.include_router(notebook.router)