from pydantic import BaseModel
from typing import List, Optional

# 프론트엔드가 보낼 요청 형식
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

# 개별 논문 응답 형식
class PaperDTO(BaseModel):
    id: int
    title: str
    abstract: str
    authors: str
    year: Optional[int] = None
    url: str
    
    # ⭐ 수정된 부분: score가 처음엔 없을 수도 있게(Optional) 설정하고 기본값을 None으로 줌
    score: Optional[float] = None 

    class Config:
        # ORM(SQLAlchemy) 객체를 Pydantic 모델로 변환 허용
        from_attributes = True

# 최종 검색 응답 리스트 형식
class SearchResponse(BaseModel):
    results: List[PaperDTO]
