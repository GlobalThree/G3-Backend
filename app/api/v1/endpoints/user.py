from fastapi import APIRouter, HTTPException, Depends

from app.schemas.user import User, UserResponse, UserCreate
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import create_user

router = APIRouter()

# 더미 데이터
users: dict[int, User] = {
    0: User(id=0, name="Jutole", email="jutole@gmail.com", password="12345678"),
}

# 유저 아이디 자동으로 넣기 위한 임의 변수
next_id: int = 1

# 이메일 중복 검사를 위한 임의 딕셔너리
email_to_id: dict[str, int] = {user.email: user.id for user in users.values()}


@router.get("/users", response_model=list[UserResponse])
async def get_users():
    return [UserResponse(**user.model_dump()) for user in users.values()]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**users[user_id].model_dump())


@router.post("/users", status_code=201)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(user=user, db=db)

    return {
        "status": "success",
        "data": {"user_id": new_user.id},
    }
