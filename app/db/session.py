from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core import config

# 데이터베이스 엔진 생성
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL,
    pool_size=5,  # 평상시 유지하는 데이터베이스 연결의 수
    max_overflow=10,  # pool_size를 초과해서 추가로 생성 가능한 연결의 수
    pool_timeout=30,  # 사용 가능한 연결을 기다리는 최대 시간
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(bind=engine, autoflush=False)


# 데이터베이스 세션을 얻기 위한 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        # db 세션을 엔드포인트에 전달
        # 엔드포인트 실행이 완료될 때까지 이 지점에서 대기
        yield db
    finally:
        # 엔드포인트 실행이 완료된 후에 실행됨
        db.close()
