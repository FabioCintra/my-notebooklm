from pathlib import Path
from backend.app import get_path_folder
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

async def delete_chat(thread_id: str):
    database_chat = get_path_folder(Path(__file__).resolve(), "app", "storage", "chats")
    database_chat = str(database_chat / "chat.db")
    
    async with AsyncSqliteSaver.from_conn_string(database_chat) as memory:
        await memory.adelete_thread(thread_id)
        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        checkpoint = await memory.aget(config)
        print(checkpoint)