from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.schemas import TaskCreate, TaskOut, TaskUpdate
from app.services.tasks import TaskService


tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@tasks_router.post("/", response_model=TaskOut, status_code=201)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = TaskService(db)
    return service.create_task(current_user.id, data)


@tasks_router.get("/", response_model=List[TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = TaskService(db)
    return service.list_tasks(current_user.id)


@tasks_router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = TaskService(db)
    return service.get_task_for_user(task_id, current_user)


@tasks_router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = TaskService(db)
    return service.update_task(task_id, data, current_user)


@tasks_router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = TaskService(db)
    service.delete_task(task_id, current_user)
    return {"message": "Задача удалена"}
