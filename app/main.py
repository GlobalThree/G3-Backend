from fastapi import FastAPI, HTTPException
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 접근 허용할 도메인 지정
    allow_credentials=True,  # 인증 정보(쿠키 등)를 허용할지 여부를 설정
    allow_methods=["*"],  # 허용할 HTTP 메서드를 지정, 여기서는 모든 메서드 허용
    allow_headers=["*"],  # 허용할 HTTP 헤더를 지정, 여기서는 모든 헤더 허용
)

memo: datetime | None = None


@app.get("/")
def main():
    return ["hello world"]


@app.post("/time")
def save_time(timestamp: datetime):
    global memo
    memo = timestamp
    return {"result": "success"}


@app.delete("/time")
def delete_time():
    global memo
    memo = None
    return {"result": "success"}


@app.get("/time")
def get_time():
    if memo is None:
        raise HTTPException(status_code=400, detail="don't save time")
    return {
        "body": {"time": memo},
    }
