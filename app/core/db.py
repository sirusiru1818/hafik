# app/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# DB 엔진 생성
engine = create_engine(settings.DATABASE_URL)

# 세션 로컬 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 베이스 클래스
Base = declarative_base()

# 의존성 주입용 함수 (API 요청 때마다 DB 열고 닫기)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
