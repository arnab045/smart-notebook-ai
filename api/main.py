from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth_api import router as auth_router
from api.note_api import router as note_router
from api.community_api import router as community_router

from api.upload_api import router as upload_router
from api.tutor_api import router as tutor_router
from api.exam_prep_api import router as exam_router 
from fastapi.staticfiles import StaticFiles
from database.models import (
    create_tables,
    create_follow_table,
    create_like_table
)

app = FastAPI()
app.mount(
    "/page-images",
    StaticFiles(
        directory="note_upload/page_images"
    ),
    name="page-images"
)
create_tables()
create_follow_table()
create_like_table()

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes

app.include_router(auth_router)
app.include_router(note_router)
app.include_router(community_router)
app.include_router(upload_router)
app.include_router(tutor_router)
app.include_router(exam_router)

@app.get("/")
def root():
    return {"message": "Smart Notebook AI Backend Running"}

app.mount(
    "/pdf",
    StaticFiles(
        directory="note_upload/pdf"
    ),
    name="pdf"
)