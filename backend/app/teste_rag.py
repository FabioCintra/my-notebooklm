import uuid
from backend.app.rag import *
from pyarrow.lib import UUID

thread_id: str = "973467af-936b-46ee-8bde-f55ed1ce3851"
question: str =  "De acordo com as tabelas de resultados, em quais cenários específicos o RAG superou o modelo paramétrico BART padrão?"

# print("##SALVANDO DOCUMENTO##")
# save_documents(thread_id)

print("RETRIEVER")
retriever = create_retriever(thread_id)
result = retriever_chunks(retriever=retriever, question=question)
for res in result:
    print(f"Score: {res['score']} \n Content: {res['content']}")


