from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.models.user import User
from fastapi import HTTPException
from app.schemas.user import UserResponse


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session) -> list[UserResponse]:
    try:
        users = db.query(User).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    user_responses = [
        UserResponse(
            email=user.email,
            name=user.name,
            id=user.id,
        )
        for user in users
    ]
    return user_responses


def get_user(id: int, db: Session) -> UserResponse:
    try:
        user: User | None = db.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(email=user.email, id=user.id, name=user.name)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


def create_user(user: user_schema.UserCreate, db: Session):
    # 이메일 중복 검사
    db_user = get_user_by_email(user.email, db=db)
    if db_user:
        raise HTTPException(status_code=409, detail="This email is not available.")

    # 새로운 User 객체 생성
    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
    )

    try:
        # 데이터베이스에 추가
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return db_user
