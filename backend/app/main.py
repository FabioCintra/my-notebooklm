from fastapi import FastAPI
from app.routers import notebook
from app.routers import llm

app = FastAPI()

app.include_router(llm.router)
app.include_router(notebook.router)