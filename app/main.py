import hashlib

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth.router import router as auth_route
from app.api.books.router import router as books_router
from app.api.models import Users
from app.api.users.router import router as user_router
from app.api.videos.router import router as video_router
from app.db import db1

admin = db1.query(Users).filter(Users.login == "admin").first()

if not admin:
    _staff = Users(
        name="admin",
        surname="admin",
        login="admin",
        password=hashlib.sha256("admin".encode()).hexdigest(),
        role="admin",
    )
    db1.add(_staff)
    db1.commit()

db1.close()

app = FastAPI()

# docs_url=None, redoc_url=None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_route, prefix="/auth", tags=["Login"])
app.include_router(router=user_router, prefix="/user", tags=["Users"])
app.include_router(router=books_router, prefix="/book", tags=["Books"])
app.include_router(router=video_router, prefix="/video", tags=["Videos"])

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
