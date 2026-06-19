from fastapi import APIRouter
from pydantic import BaseModel

from ai_assistant.exam_prep_backend import prepare_exam

router = APIRouter()

class ExamPrepRequest(BaseModel):
    note_text: str

@router.post("/prepare-exam")
def prepare_exam_route(data: ExamPrepRequest):

    result = prepare_exam(data.note_text)

    return {
        "result": result
    }