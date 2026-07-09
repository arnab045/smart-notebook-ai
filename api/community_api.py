from fastapi import APIRouter

from database.models import (
    get_public_notes,
    count_likes,
    count_comments,
    toggle_like,
    has_liked,
    add_comment,
    get_comments,
    save_note
)

router = APIRouter()


# =========================
# GET COMMUNITY POSTS
# =========================

@router.get("/community/posts")
def fetch_community_posts(user_email: str = ""):

    notes = get_public_notes()

    formatted_posts = []

    for note in notes:

        formatted_posts.append({

            "id": note[0],
            "title": note[1],
            "subject": note[2],
            "content": note[3],
            "user_email": note[4],

            "likes": count_likes(note[0]),

            "comments": count_comments(note[0]),

            "liked": has_liked(
                note[0],
                user_email
            )

        })

    return {

        "success": True,
        "posts": formatted_posts

    }

    return {

        "success": True,
        "posts": formatted_posts

    }

from pydantic import BaseModel

class LikeRequest(BaseModel):

    note_id: int
    user_email: str


@router.post("/community/like")
def like_post(request: LikeRequest):

    liked, total_likes = toggle_like(

        request.note_id,
        request.user_email

    )

    return {

        "success": True,

        "liked": liked,

        "likes": total_likes

    }

from pydantic import BaseModel

class CommentRequest(BaseModel):

    note_id: int
    user_email: str
    comment: str

class SaveRequest(BaseModel):

    user_email: str
    title: str
    subject: str
    content: str


@router.post("/community/comment")
def comment_post(request: CommentRequest):

    add_comment(
        request.note_id,
        request.user_email,
        request.comment
    )

    comments = get_comments(request.note_id)

    return {

        "success": True,

        "comments": [

            {

                "user_email": c[0],

                "comment": c[1]

            }

            for c in comments

        ]

    }

@router.get("/community/comments/{note_id}")
def fetch_comments(note_id: int):

    comments = get_comments(note_id)

    return {

        "success": True,

        "comments": [

            {

                "user_email": c[0],

                "comment": c[1]

            }

            for c in comments

        ]

    }

@router.post("/community/save")
def save_from_community(request: SaveRequest):

    save_note(

        request.user_email,

        request.title,

        request.subject,

        request.content,

        "",     # original_file_path

        "",     # pdf_path

        "community"

    )

    return {

        "success": True,

        "message": "Note saved successfully"

    }