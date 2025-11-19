import os
import psycopg2
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from openai import OpenAI
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

# .env 파일 로드 (환경변수 관리)
load_dotenv()

# 1. 경로 설정 (기존 코드 유지: 중요!)
# hafik/app/main.py 위치를 기준으로 상위 폴더를 잡습니다.
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. 환경 변수 및 설정
# 실제 배포시에는 .env 파일에 넣거나 환경변수로 설정해야 합니다.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...") # 여기에 API 키 입력
DB_HOST = os.getenv("DB_HOST", "database-1.xxxx.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

app = FastAPI(
    title="Hafik AI Research Assistant",
    version="1.0.0",
)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

# 3. 정적 파일 마운트 (기존 코드 유지)
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend" / "public"),
    name="static"
)

# 4. 데이터베이스 연결 함수
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    register_vector(conn)
    return conn

# 5. 임베딩 함수
def get_embedding(text):
    # 텍스트가 너무 길면 자르거나 에러 처리가 필요할 수 있음
    response = client.embeddings.create(
        input=text.replace("\n", " "),
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# 6. 메인 페이지 서빙 (기존 코드 유지 + 경로 수정)
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    # frontend/public/index.html 경로를 정확히 찾아갑니다.
    index_file_path = BASE_DIR / "frontend" / "public" / "index.html"
    
    if not index_file_path.exists():
        return "<html><body><h1>Error: index.html not found!</h1></body></html>"
        
    with open(index_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

# 7. 검색 API (새로 추가된 기능)
@app.get("/api/v1/search")
async def search_papers(q: str):
    try:
        # A. 가설을 벡터로 변환
        query_vector = get_embedding(q)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # B. RDS 검색 쿼리 (유사도 높은 순)
        # 만약 테이블 이름이 다르다면 'papers'를 실제 테이블명으로 바꿔주세요.
        sql = """
            SELECT id, title, abstract, url, authors, published_year, 
                   1 - (embedding <=> %s::vector) as similarity
            FROM papers
            ORDER BY embedding <=> %s::vector
            LIMIT 5;
        """
        
        cur.execute(sql, (query_vector, query_vector))
        rows = cur.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "title": row[1],
                "abstract": row[2],
                "url": row[3],
                "authors": row[4] if row[4] else "Unknown",
                "year": row[5] if row[5] else 2024,
                "similarity": int(row[6] * 100)
            })
            
        cur.close()
        conn.close()
        
        return results

    except Exception as e:
        print(f"Search Error: {e}")
        # 에러가 나도 프론트가 멈추지 않게 JSON 에러 반환
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Hafik Backend"}