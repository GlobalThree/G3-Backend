from fastapi import APIRouter, Depends

from app.schemas.user import UserResponse, UserCreate
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import create_user, get_users, get_user

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
async def get_users_endpoint(db: Session = Depends(get_db)):
    return [UserResponse(**user.model_dump()) for user in get_users(db=db)]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(id=user_id, db=db)


@router.post("/users", status_code=201)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(user=user, db=db)

    return {
        "status": "success",
        "data": {"user_id": new_user.id},
    }
