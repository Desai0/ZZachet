from fastapi import FastAPI

from app.database import Base, SessionLocal, engine
from app.repositories import UserRepository
from app.routers.admin import admin_router
from app.routers.auth import auth_router
from app.routers.tasks import tasks_router

app = FastAPI(title="Task Tracker API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        repo = UserRepository(db)
        admin = repo.get_by_username("admin")
        if not admin:
            repo.create(
                email="admin@example.com",
                username="admin",
                phone="+7-900-000-00-00",
                password="Admin123",
                role="admin"
            )
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Task Tracker API is running"}


app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(admin_router)
