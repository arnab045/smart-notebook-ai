from fastapi import APIRouter
from pydantic import BaseModel

from database.models import save_quiz_result

router = APIRouter()


class QuizResultRequest(BaseModel):

    user_email: str

    subject: str

    score: int

    total_questions: int

    percentage: float


@router.post("/quiz/save-result")
def save_result(request: QuizResultRequest):

    save_quiz_result(

        request.user_email,

        request.subject,

        request.score,

        request.total_questions,

        request.percentage

    )

    return {

        "success": True

    }