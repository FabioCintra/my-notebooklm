import uuid
from typing import TypedDict,Literal
import os
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel
from app.rag import create_retriever, retriever_chunks,summarize_chunks

load_dotenv()

# connection = create_connection()
# memory = AsyncSqliteSaver(connection)

#========================
# STATES
#========================

class InternalState(MessagesState):
    #messages
    best_chunks: list[str]
    route: Literal["no_rag", "retriever", "summary"]
    thread_id: str

class OutputState(TypedDict):
    answer: str

class RouteModel(BaseModel):
    route: Literal["no_rag", "retriever", "summary"]

#========================
# LLM
#========================

llm = ChatOllama(
    model=os.getenv("model"),
    base_url=os.getenv("base_url"),
    temperature=0.1,
)

route_llm = llm.with_structured_output(RouteModel, include_raw=False)


#========================
# NODES
#========================
def check_prompt(state: InternalState):
    question = state["messages"][-1].content
    context = "\n\n".join(message.content for message in state["messages"][-10:-1])

    prompt = f"""
        You are a router for a document-grounded question answering system.

        Conversation context:
        {context}

        User question:
        {question}

        Choose exactly one route:

        - "summary":
        Use when the user explicitly asks to summarize, synthesize,
        give an overview, list the main points, or broadly explain
        the documents/content.

        - "retriever":
        Use for ANY informational or knowledge question whose answer
        should be grounded in the user's documents.

        This includes:
        - "What is X?"
        - "What does X mean?"
        - "How does X work?"
        - "Why does X happen?"
        - "Explain X"
        - comparisons
        - definitions
        - factual questions
        - conceptual questions
        - questions about a specific topic

        IMPORTANT:
        The fact that you already know the answer from your pretrained
        knowledge is IRRELEVANT. This system must prefer the documents.

        - "no_rag":
        Use ONLY for messages that do not require document knowledge.

        Examples:
        - "hello"
        - "good morning"
        - "thank you"
        - "what is my name?" when the name was explicitly stated
        in the conversation
        - casual conversation
        - questions about the conversation itself

        Examples:

        User: "O que é Retrieval-Augmented Generation, ou RAG?"
        Route: retriever

        User: "O que é inteligência artificial?"
        Route: retriever

        User: "Como funciona RAG?"
        Route: retriever

        User: "Qual a diferença entre RAG e fine-tuning?"
        Route: retriever

        User: "Resuma os documentos."
        Route: summary

        User: "Quais são os principais pontos do material?"
        Route: summary

        User: "Olá!"
        Route: no_rag

        User: "Obrigado."
        Route: no_rag

        Rules:
        - NEVER choose no_rag simply because you know the answer.
        - Informational questions default to retriever.
        - If uncertain between retriever and no_rag, choose retriever.
        - Do not answer the question.
        - Only classify it.
    """
    response = route_llm.invoke([HumanMessage(content=prompt)])

    return {
        "route": response.route
    }

def route_node(state: InternalState):
    if state["route"] == "retriever":
        return "best_chunks_with_window_context"

    if state["route"] == "summary":
        return "best_chunks_summarized"

    return "generate_answer"

def best_chunks_summarized(state: InternalState):
    question = state["messages"][-1].content
    thread_id = uuid.UUID(state["thread_id"])
    answer = summarize_chunks(thread_id, question)

    return {
        "messages": [
            AIMessage(content=answer)
        ]
    }

def best_chunks_with_window_context(state: InternalState):
    question = state["messages"][-1].content
    thread_id = uuid.UUID(state["thread_id"])

    retriever = create_retriever(thread_id)
    best_chunks = retriever_chunks(retriever, question)

    return {
        "best_chunks": best_chunks
    }

def generate_answer(state: InternalState):
    last_message = state["messages"][-1].content

    context = "\n\n".join(message.content for message in state["messages"][-10:-1])

    system_prompt = """
        You are an assistant specialized in answering the user's questions accurately using the provided context.

        Rules:
        - Base your answer on the retrieved document context when it is available.
        - Use the conversation history only when it is relevant to understanding the user's question.
        - You may summarize, paraphrase, combine, and explain information that is clearly supported by the provided context.
        - Do not introduce facts, assumptions, or conclusions that are not supported by the provided information.
        - Do not require the answer to appear verbatim in the context. A valid answer may be derived by clearly connecting information present in the context.
        - If the context does not contain enough information to answer the question reliably, clearly say that there is not enough information.
        - Prefer a complete and explanatory answer over simply copying sentences from the context.
        - Answer naturally and directly.
        - Do not mention retrieved documents, chunks, retrieval, RAG, prompts, or internal reasoning.
        - Avoid unnecessary formatting unless the user explicitly requests it.
    """

    prompt = f"""
        Conversation context:
        {context}
        
        User message:
        {last_message}
    """

    if state["route"] == "retriever":
        best_chunks = state["best_chunks"]

        documents_context = "\n\n".join(
            chunk["content"]
            for chunk in best_chunks
        )

        prompt += f"""
        
            Relevant information retrieved from the user's documents:
            {documents_context}
            
            Use this retrieved information as the primary source for answering the user's message.
        """

    prompt += f"""
        Generate the final response to the user.
    """

    result: str = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])

    return {
        "messages": [
            AIMessage(content=result.content)
        ]
    }

def final_node(state: InternalState):
    answer = state["messages"][-1].content

    return {
        "answer": answer
    }

def generate_graph(memory):
    builder = StateGraph(InternalState, output_schema=OutputState)

    builder.add_node("check_prompt",check_prompt)
    builder.add_node("best_chunks_summarized",best_chunks_summarized)
    builder.add_node("best_chunks_with_window_context",best_chunks_with_window_context)
    builder.add_node("generate_answer",generate_answer)
    builder.add_node("final_node", final_node)

    builder.add_edge(START, "check_prompt")
    builder.add_conditional_edges("check_prompt",route_node)
    builder.add_edge("best_chunks_summarized","final_node")
    builder.add_edge("best_chunks_with_window_context","generate_answer")
    builder.add_edge("generate_answer","final_node")
    builder.add_edge("final_node", END)

    return builder.compile(checkpointer=memory)








