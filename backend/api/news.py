"""
뉴스 API 라우터
"""

from fastapi import APIRouter, Query, HTTPException
import sys
from pathlib import Path

# 부모 디렉토리를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.news_service import NewsService

router = APIRouter()
service = NewsService()


@router.get("/stock-news", tags=["News Search"])
async def get_stock_news(ticker: str = Query(..., description="종목 코드"), limit: int = Query(5, description="결과 개수")):
    """
    주식 관련 뉴스 검색
    
    Parameters:
    - ticker: 종목 코드 (예: AAPL, MSFT, NVDA)
    - limit: 결과 개수 (기본값: 5)
    
    Returns:
    - 검색된 뉴스 목록 (제목, URL, 발행일, 요약)
    """
    result = await service.search_stock_news(ticker, limit)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@router.get("/", tags=["News Search"])
async def get_market_news(limit: int = Query(10, description="결과 개수")):
    """
    시장 관련 뉴스 조회 (최근 24시간)
    
    Parameters:
    - limit: 결과 개수 (기본값: 10)
    
    Returns:
    - 시장 뉴스 목록
    """
    result = await service.get_market_news(limit)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@router.get("/search", tags=["News Search"])
async def search_news(query: str = Query(..., description="검색 쿼리"), limit: int = Query(10, description="결과 개수")):
    """
    뉴스 검색 (향후 구현)
    
    Parameters:
    - query: 검색 쿼리
    - limit: 결과 개수
    
    Returns:
    - 검색 결과
    """
    return {
        "message": "뉴스 검색",
        "query": query,
        "limit": limit,
        "results": []
    }

