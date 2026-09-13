from typing import Dict

from fastapi import APIRouter, status

from app.schemas.llm import AnswerResponse, AnswerRequest
from app.services.llm import get_chat_answer

router = APIRouter(
    prefix="/llms",
    tags=["LLMS"]
)

@router.post("/", status_code=status.HTTP_200_OK)
async def answer_of_question(request: AnswerRequest) -> AnswerResponse:
    thread_id: str = str(request.thread_id)
    prompt: str = request.prompt
    config: Dict[str,Dict[str,str]] = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await get_chat_answer(thread_id=thread_id, prompt=prompt, config=config)

    return AnswerResponse(answer=result)



