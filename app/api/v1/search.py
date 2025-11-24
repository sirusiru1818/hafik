# app/api/v1/search.py
import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.search import SearchRequest, SearchResponse, PaperDTO
from app.services.search import search_similar_papers

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
def search_papers_endpoint(request: SearchRequest, db: Session = Depends(get_db)):
    try:
        print(f"🔍 Searching for: {request.query}")
        
        # 서비스에서 (논문, 거리값) 튜플을 받아옴
        papers_with_scores = search_similar_papers(db, request.query, request.top_k)
        print(f"✅ Found {len(papers_with_scores)} papers")
        
        results = []
        for paper, distance in papers_with_scores:
            # Pydantic 모델로 변환
            paper_dto = PaperDTO.model_validate(paper)
            
            # 거리(0~2)를 유사도 퍼센트(0~100%)로 변환
            # 거리가 0이면 100점, 거리가 멀수록 점수가 깎임
            similarity_score = (1 - distance) * 100
            
            # 소수점 1자리까지만 (예: 87.5)
            paper_dto.score = round(similarity_score, 1)
            
            results.append(paper_dto)
        
        return SearchResponse(results=results)
        
    except Exception as e:
        print("❌ CRITICAL ERROR OCCURRED:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
