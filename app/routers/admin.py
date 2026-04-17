from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_admin, get_db
from app.schemas import UserOut
from app.repositories import UserRepository


admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.get("/users", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin)
):
    return UserRepository(db).list_all()
