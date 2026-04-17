from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Task, User
from app.security import hash_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_login(self, login: str):
        return self.db.query(User).filter(
            or_(User.email == login, User.username == login)
        ).first()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def list_all(self):
        return self.db.query(User).all()

    def create(self, email: str, username: str, phone: str, password: str, role: str = "user"):
        user = User(
            email=email,
            username=username,
            phone=phone,
            hashed_password=hash_password(password),
            role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, owner_id: int, title: str, description: str = ""):
        task = Task(
            owner_id=owner_id,
            title=title,
            description=description,
            status="new"
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def list_by_owner(self, owner_id: int):
        return self.db.query(Task).filter(Task.owner_id == owner_id).all()

    def update(self, task: Task):
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()
