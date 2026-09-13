import os
import asyncio

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from .agent import generate_graph

config = {
    "configurable": {
        "thread_id": "1c7a18cb-daea-43bb-a7d2-12d30dbe3fb9"
    }
}

config2 = {
    "configurable": {
        "thread_id": "321ee9a2-712b-4713-b080-946f0aced419"
    }
}

async def main():
    os.makedirs("D:\\pycharm\\my-notebooklm\\app\\database\\state_db", exist_ok=True)
    async with AsyncSqliteSaver.from_conn_string(
            "D:\\pycharm\\my-notebooklm\\app\\database\\state_db\\conversation_history.db"
    ) as memory:

        #save_documents(uuid.UUID("321ee9a2-712b-4713-b080-946f0aced419"))


        graph = generate_graph(memory=memory)

        # async for event in graph.astream_events(
        #     input={
        #         "messages": [
        #             HumanMessage(content="Como as funções GOVERN, MAP, MEASURE e MANAGE se relacionam?")
        #         ],
        #         "thread_id": "321ee9a2-712b-4713-b080-946f0aced419"
        #     },
        #     config=config,
        #     version="v2"
        # ):
        #     if event["event"] == "on_chat_model_stream" and event["metadata"].get("langgraph_node", '') == "generate_answer":
        #         data = event["data"]
        #         print(data["chunk"].content, end="")

        result = await graph.ainvoke(
            input={
                "messages": [
                    HumanMessage(content="O que é Retrieval-Augmented Generation, ou RAG?")
                ],
                "thread_id": "1c7a18cb-daea-43bb-a7d2-12d30dbe3fb9"
            },
            config=config
        )

        print(result["answer"])

asyncio.run(main())

