# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.search import router as search_router

app = FastAPI(title="Hafik Service")

# CORS 설정 (프론트엔드가 다른 서버/파일일 경우 필수)
# 로컬 개발을 위해 모든 출처(["*"]) 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(search_router, prefix="/api/v1", tags=["search"])

@app.get("/")
def root():
    return {"message": "Hafik API is running successfully!"}
