"""
While You Were Sleeping - FastAPI 메인 애플리케이션
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="While You Were Sleeping API",
    description="미국 주식 데일리 브리핑 서비스 API",
    version="1.0.0"
)

# CORS 설정
# 프론트엔드 localhost:3000에서의 접근 허용
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # 필요한 메서드만 허용
    allow_headers=["*"],
)


# 헬스 체크 엔드포인트
@app.get("/", tags=["Health"])
async def root():
    """API 상태 확인"""
    return {
        "status": "ok",
        "service": "While You Were Sleeping API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


# 라우터 임포트
from api import stocks, news, briefings


# 라우터 등록
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(news.router, prefix="/api/news", tags=["News"])
app.include_router(briefings.router, tags=["Briefing"])


if __name__ == "__main__":
    import uvicorn
    
    # 개발 환경에서 실행
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
