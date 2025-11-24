import os
from dotenv import load_dotenv

# .env 파일 로드 (이 부분이 없으면 AWS 주소를 못 가져오고 localhost로 접속합니다)
load_dotenv()

class Settings:
    # 환경 변수가 없으면 기본값으로 localhost를 쓰게 되어 있는데,
    # AWS 주소가 잘 로드되면 그 주소를 사용하게 됩니다.
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost") # 여기가 문제였습니다!
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    
    # SQLAlchemy용 DB URL 생성
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()
