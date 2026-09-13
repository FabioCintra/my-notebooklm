from pathlib import Path
from app import get_path_folder
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

DATABASE_CHAT = str(
    get_path_folder(Path(__file__).resolve(), "app", "storage", "chats") / "chat.db"
)

async def delete_chat(thread_id: str):    
    async with AsyncSqliteSaver.from_conn_string(DATABASE_CHAT) as memory:
        await memory.adelete_thread(thread_id)

async def messages_chat(thread_id: str):
    async with AsyncSqliteSaver.from_conn_string(DATABASE_CHAT) as memory:
        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        result = await memory.aget(config)

        messages = result["channel_values"]["messages"]

        return messages

