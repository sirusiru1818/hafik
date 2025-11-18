# Hafik Project

+==================+
|  GitHub Command  |
+==================+

### Check the current status of files
git status

### Add everything, including README
git add .

### Commit
git commit -m "Message"

### Initial push to GitHub
git push -u origin main


### Directory Structure
hafik/
├─ app/                      # 🔹 FastAPI 백엔드
│  ├─ main.py                # FastAPI 엔트리포인트
│  ├─ api/
│  │  ├─ __init__.py
│  │  └─ v1/
│  │     ├─ __init__.py
│  │     └─ search.py        # /api/v1/search 엔드포인트
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py           # 환경설정 (DB_URL, 모델명)
│  │  └─ db.py               # PostgreSQL + pgvector 연결
│  ├─ models/
│  │  ├─ __init__.py
│  │  └─ paper.py            # 논문 테이블 + vector 컬럼
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  └─ search.py           # Request/Response Pydantic 모델
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ embeddings.py       # 임베딩 생성
│  │  └─ search.py           # pgvector 검색 로직
│  └─ __init__.py
│
├─ frontend/                 # 🔹 프론트엔드 (HTML/CSS/JS)
│  ├─ index.html             # 검색 UI (가설 입력)
│  ├─ styles.css             # 스타일
│  └─ main.js                # JS → 백엔드 API 호출
│
├─ scripts/                  # 데이터 적재 등 유틸
│  └─ load_papers.py
│
├─ tests/                    # 테스트 코드
│  └─ __init__.py
│
├─ .env                      # 환경변수 (gitignore 대상)
├─ .gitignore
├─ requirements.txt
└─ README.md
