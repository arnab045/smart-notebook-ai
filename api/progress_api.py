from fastapi import APIRouter

from database.models import get_progress_overview

router = APIRouter()


@router.get("/progress/overview")
def progress_overview(user_email: str):

    data = get_progress_overview(user_email)

    return {

        "success": True,

        "data": data

    }