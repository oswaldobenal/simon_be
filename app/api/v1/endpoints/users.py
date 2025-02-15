from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.session import get_db
from app.schemas.v1.users import UserCreate, UserOut
from app.services.users import UserService

router = APIRouter()


@router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    if service.get_user_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    return service.create_user(user_in)
