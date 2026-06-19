from fastapi import APIRouter

from database.models import (
    get_public_notes,
    count_likes
)

router = APIRouter()


# =========================
# GET COMMUNITY POSTS
# =========================

@router.get("/community/posts")
def fetch_community_posts():

    notes = get_public_notes()

    formatted_posts = []

    for note in notes:

        formatted_posts.append({

            "id": note[0],
            "title": note[1],
            "subject": note[2],
            "content": note[3],
            "user_email": note[4],
            "likes": count_likes(note[0])

        })

    return {

        "success": True,
        "posts": formatted_posts

    }