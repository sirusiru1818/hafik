import os
import json
import psycopg2
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일)
load_dotenv()

# --- 설정 ---
# 프로젝트 루트에서 실행한다고 가정: data 폴더나 같은 위치에 json 파일이 있어야 함
# 만약 json 파일이 다른 곳에 있다면 절대 경로를 입력하세요.
DATA_PATH = "arxiv-metadata-oai-snapshot.json" 
BATCH_SIZE = 32
LIMIT = 1000  # 테스트용 1000개. 전체를 하려면 None으로 변경

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def main():
    # M2 가속 확인
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"🚀 Using device: {device}")

    # 모델 로드
    print("📥 Loading model (all-mpnet-base-v2)...")
    model = SentenceTransformer('all-mpnet-base-v2', device=device)

    # DB 연결
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("✅ Connected to Database")
    except Exception as e:
        print("❌ DB Connection Failed:", e)
        return

    batch_data = []
    count = 0
    
    print(f"📂 Reading data from {DATA_PATH}...")
    
    try:
        with open(DATA_PATH, 'r') as f:
            for line in tqdm(f):
                if LIMIT and count >= LIMIT:
                    break
                    
                paper = json.loads(line)
                
                # 필요한 정보 추출
                paper_id = paper.get('id')
                title = paper.get('title', '').replace('\n', ' ').strip()
                abstract = paper.get('abstract', '').replace('\n', ' ').strip()
                authors = paper.get('authors', '').strip()
                
                try:
                    versions = paper.get('versions', [])
                    year = int(versions[-1]['created'].split()[3]) 
                except:
                    year = None
                
                url = f"https://arxiv.org/abs/{paper_id}"
                text_to_embed = f"{title}. {abstract}"
                
                batch_data.append({
                    'title': title,
                    'abstract': abstract,
                    'authors': authors,
                    'year': year,
                    'url': url,
                    'text': text_to_embed
                })

                if len(batch_data) >= BATCH_SIZE:
                    process_batch(batch_data, model, cursor)
                    conn.commit()
                    batch_data = []
                
                count += 1

        if batch_data:
            process_batch(batch_data, model, cursor)
            conn.commit()

        print(f"🎉 Finished! Total {count} papers inserted.")

    except FileNotFoundError:
        print(f"❌ Error: '{DATA_PATH}' file not found. Please check the path.")
    finally:
        cursor.close()
        conn.close()

def process_batch(batch, model, cursor):
    texts = [item['text'] for item in batch]
    embeddings = model.encode(texts, show_progress_bar=False)

    for item, vector in zip(batch, embeddings):
        cursor.execute("""
            INSERT INTO papers (title, abstract, authors, year, url, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            item['title'],
            item['abstract'],
            item['authors'],
            item['year'],
            item['url'],
            vector.tolist()
        ))

if __name__ == "__main__":
    main()
