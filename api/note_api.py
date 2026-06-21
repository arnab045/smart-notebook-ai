from fastapi import APIRouter
from pydantic import BaseModel

from note_analysis.missing_points_backend import detect_missing_points
from note_analysis.improve_backend import improve_note
from ai_assistant.quiz_generator_backend import generate_quiz

from database.models import (
    save_note,
    get_user_notes,
    get_note_by_id,
    get_profile,
    get_follower_count,
    get_following_count,
    get_public_notes_by_user,
    update_profile,
    make_note_public,
    get_note_page_images
)


router = APIRouter()


# =========================
# REQUEST MODEL
# =========================

class NoteRequest(BaseModel):

    user_email: str
    title: str
    subject: str
    content: str

    original_file_path: str
    pdf_path: str
    file_type: str

    num_questions: int = 10

class QuizRequest(BaseModel):

    content: str

    num_questions: int = 10

class ProfileRequest(BaseModel):

    email: str

    bio: str

    university: str

    department: str

    skills: str


# =========================
# SAVE NOTE
# =========================

@router.post("/save-note")
def create_note(request: NoteRequest):

    save_note(
        request.user_email,
        request.title,
        request.subject,
        request.content,
        request.original_file_path,
        request.pdf_path,
        request.file_type
    )

    return {
        "success": True,
        "message": 
            "Note saved successfully"
    }


# =========================
# GET USER NOTES
# =========================

@router.get("/my-notes/{user_email}")
def fetch_notes(user_email: str):

    notes = get_user_notes(user_email)

    formatted_notes = []

    for note in notes:

        formatted_notes.append({

            "id": note[0],
            "title": note[1],
            "subject": note[2]

        })

    return {
        "success": True,
        "notes": formatted_notes
    }


# =========================
# GET SINGLE NOTE
# =========================

@router.get("/note/{note_id}")
def fetch_note(note_id: int):

    note = get_note_by_id(note_id)

    if not note:

        return {
            "success": False,
            "message": "Note not found"
        }

    page_images = get_note_page_images(
        note[3]
    )

    return {

        "success": True,

        "note": {

            "title": note[0],
            "subject": note[1],
            "content": note[2],
            "pdf_path": note[3],

            "page_images":
                page_images

        }

    }

@router.post("/analyze-note")
def analyze_note(request: NoteRequest):

    result = detect_missing_points(
        request.content
    )

    return {

        "success": True,
        "analysis": result

    } 

@router.post("/improve-note")
def improve_existing_note(request: NoteRequest):

    improved = improve_note(
        request.content
    )

    return {

        "success": True,
        "improved_content": improved

    } 

@router.post("/generate-quiz")
def create_quiz(request: QuizRequest):

    quiz = generate_quiz(
        request.content,
        request.num_questions
    )

    return {

        "success": True,
        "quiz": quiz

    }

# =========================
# GET PROFILE
# =========================

@router.get("/profile/{email}")
def fetch_profile(email: str):

    profile = get_profile(email)

    if not profile:

        return {
            "success": False,
            "message": "Profile not found"
        }

    followers = get_follower_count(email)

    following = get_following_count(email)

    public_notes = get_public_notes_by_user(email)

    return {

        "success": True,

        "profile": {

            "full_name": profile[0],
            "email": profile[1],

            "bio": profile[2],
            "university": profile[3],
            "department": profile[4],
            "skills": profile[5],

            "followers": followers,
            "following": following,

            "notes_shared":
                len(public_notes)
        }

    }

# =========================
# UPDATE PROFILE
# =========================

@router.post("/update-profile")
def save_profile(request: ProfileRequest):

    update_profile(

        request.email,

        request.bio,

        request.university,

        request.department,

        request.skills

    )

    return {

        "success": True,

        "message":
            "Profile updated successfully"

    }

# =========================
# SHARE NOTE TO COMMUNITY
# =========================

@router.post("/make-public/{note_id}")
def share_note(note_id: int):

    make_note_public(note_id)

    return {

        "success": True,

        "message":
            "Note shared successfully"

    }

# =========================
# COMMUNITY POSTS
# =========================

@router.get("/community-posts")
def fetch_community_posts():

    notes = get_public_notes()

    posts = []

    for note in notes:

        posts.append({

            "id": note[0],
            "title": note[1],
            "subject": note[2],
            "content": note[3],
            "user_email": note[4]

        })

    return {

        "success": True,
        "posts": posts

    }