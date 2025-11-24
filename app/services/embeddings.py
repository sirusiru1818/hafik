# app/services/embeddings.py
from sentence_transformers import SentenceTransformer
import torch

# 전역 변수로 모델 로드 (서버 시작 시 한 번만 로딩)
# M2 맥북 가속(mps) 사용
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"🔄 Loading Embedding Model on {device}...")
model = SentenceTransformer('all-mpnet-base-v2', device=device)
print("✅ Model Loaded!")

def get_query_embedding(query: str) -> list:
    """
    텍스트 쿼리를 입력받아 768차원 벡터(list)로 반환
    """
    # convert_to_tensor=False -> numpy array -> tolist()
    return model.encode(query, show_progress_bar=False).tolist()
