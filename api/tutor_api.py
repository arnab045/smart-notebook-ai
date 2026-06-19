from fastapi import APIRouter
from pydantic import BaseModel

from ai_assistant.tutor_chat_backend import ask_tutor

router = APIRouter()


class TutorRequest(BaseModel):
    note_text: str
    question: str
    chat_history: str = ""


@router.post("/tutor-chat")
def tutor_chat(data: TutorRequest):

    answer = ask_tutor(
        data.note_text,
        data.chat_history,
        data.question
    )

    return {
        "answer": answer
    }