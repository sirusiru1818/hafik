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
│  ├─ __init__.py
│  ├─ main.py                # FastAPI 엔트리포인트
│  ├─ api/
│  │  ├─ __init__.py
│  │  └─ v1/
│  │     ├─ __init__.py
│  │     └─ search.py        # /api/v1/search 엔드포인트
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py           # 환경설정 (DB_URL, MODEL_NAME 등)
│  │  └─ db.py               # PostgreSQL + pgvector 연결
│  ├─ models/
│  │  ├─ __init__.py
│  │  └─ paper.py            # 논문 테이블 + vector 컬럼
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  └─ search.py           # Request/Response Pydantic 모델
│  └─ services/
│     ├─ __init__.py
│     ├─ embeddings.py       # sentence-transformers 임베딩
│     └─ search.py           # pgvector 검색 로직
│
├─ frontend/                 # 🔹 프론트엔드 (HTML/CSS/JS)
│  ├─ public/
│  │  └─ index.html          # 검색 UI 페이지
│  └─ src/
│     ├─ css/
│     │  └─ styles.css       # 스타일
│     └─ js/
│        └─ main.js          # 백엔드 API 호출 JS
│
├─ scripts/                  # 🔹 유틸 스크립트 (로컬 개발/데이터 준비)
│  ├─ __init__.py
│  ├─ load_papers.py         # 논문 메타데이터 DB에 적재
│  ├─ create_embeddings.py   # 논문 임베딩 생성 후 DB 저장
│  └─ init_db.py             # DB 초기화 (테이블 생성 등)
│
├─ tests/                    # 🔹 테스트 코드
│  ├─ __init__.py
│  ├─ conftest.py            # pytest 설정
│  ├─ test_api/
│  │  ├─ __init__.py
│  │  └─ test_search.py
│  └─ test_services/
│     ├─ __init__.py
│     └─ test_embeddings.py
│
├─ .env                      # 환경변수 파일 (GitHub 업로드 금지)
├─ .env.example              # 템플릿 (GitHub 업로드 가능)
├─ .gitignore
├─ requirements.txt
└─ README.md
