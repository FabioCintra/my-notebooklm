import os
from typing import Dict
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.agent import *
from app.utils import get_path_folder

load_dotenv()

async def get_chat_answer(thread_id: str, prompt: str, config: Dict[str, Dict[str,str]]) -> str:

    result: str = ""

    database_chat = get_path_folder(Path(__file__).resolve(), "app", "storage", "chats")
    database_chat = str(database_chat / "chat.db")

    async with AsyncSqliteSaver.from_conn_string(database_chat) as memory:
        graph = generate_graph(memory)

        result = await graph.ainvoke(
            input={
                "messages": [
                    HumanMessage(content=prompt)
                ],
                "thread_id": thread_id,
            },
            config=config
        )

    return result["answer"]

