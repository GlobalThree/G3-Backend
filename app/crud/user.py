from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.models.user import User
from fastapi import HTTPException


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


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
