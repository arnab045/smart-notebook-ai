from fastapi import APIRouter
from pydantic import BaseModel

from database.models import create_user, login_user

router = APIRouter()


# =========================
# Request Models
# =========================

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# =========================
# Signup Route
# =========================

@router.post("/signup")
def signup(request: SignupRequest):

    result = create_user(
        request.name,
        request.email,
        request.password
    )

    if result:

        return {
            "success": True,
            "message": "Account created successfully"
        }

    return {
        "success": False,
        "message": "Email already exists"
    }


# =========================
# Login Route
# =========================

@router.post("/login")
def login(request: LoginRequest):

    user = login_user(
        request.email,
        request.password
    )

    if user:

        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "name": user[1],
                "email": user[2]
            }
        }

    return {
        "success": False,
        "message": "Invalid email or password"
    }