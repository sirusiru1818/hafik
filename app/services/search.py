# app/services/search.py
from sqlalchemy.orm import Session
from app.models.paper import Paper
from app.services.embeddings import get_query_embedding

def search_similar_papers(db: Session, query: str, top_k: int = 5):
    # 1. 쿼리 임베딩 생성
    query_vector = get_query_embedding(query)

    # 2. 거리 계산 (distance)를 포함해서 조회
    # label("distance")는 계산된 거리값에 이름을 붙여주는 것입니다.
    results = db.query(Paper, Paper.embedding.cosine_distance(query_vector).label("distance"))\
        .order_by(Paper.embedding.cosine_distance(query_vector))\
        .limit(top_k).all()

    return results  # [(Paper객체, 0.152), (Paper객체, 0.214)...] 형태로 반환됨
