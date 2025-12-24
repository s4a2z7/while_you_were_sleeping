"""
주식 API 라우터
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Literal
import sys
from pathlib import Path
from datetime import datetime

# 부모 디렉토리를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.stock_service import StockService
from services.news_service import NewsService
from models.schemas import TrendingStockDetail, NewsItem

router = APIRouter()
stock_service = StockService()
news_service = NewsService()

# 스크리너 타입 리터럴
ScreenerType = Literal["most_actives", "day_gainers", "day_losers"]


@router.get("/trending", tags=["Stock Screener"])
async def get_trending_stocks(screener_type: ScreenerType = Query("most_actives", description="스크리너 타입")):
    """
    화제 종목 조회 (상위 1개 + 관련 뉴스)
    
    Parameters:
    - screener_type: most_actives (가장 거래량이 많은 종목), day_gainers (당일 상승), day_losers (당일 하락)
    
    Returns:
    - 선정된 TOP 1 종목의 상세 정보 + 관련 뉴스
    """
    try:
        # 종목 정보 조회
        stock_result = await stock_service.get_trending_stocks(screener_type)
        
        if stock_result.get("status") == "error":
            raise HTTPException(status_code=400, detail=stock_result.get("message", "주식 조회 실패"))
        
        # TOP 종목 추출
        top_stock = stock_result.get("top_stock", {})
        ticker = top_stock.get("ticker")
        
        # 관련 뉴스 조회 (5개)
        news_result = await news_service.search_stock_news(ticker, limit=5)
        news_list = []
        
        if news_result.get("status") == "success":
            for news in news_result.get("news", []):
                try:
                    # published_date를 datetime으로 변환
                    pub_date = news.get("published_date", "")
                    if isinstance(pub_date, str) and pub_date:
                        try:
                            published_at = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                        except ValueError:
                            published_at = datetime.now()
                    else:
                        published_at = datetime.now()
                    
                    news_item = NewsItem(
                        title=news.get("title", ""),
                        summary=news.get("summary", ""),
                        source="Exa",
                        url=news.get("url", ""),
                        published_at=published_at,
                        related_tickers=[ticker]
                    )
                    news_list.append(news_item)
                except (KeyError, ValueError, TypeError) as e:
                    # 개별 뉴스 파싱 오류 무시
                    pass
        
        # 통합 응답 구성
        response = {
            "status": "success",
            "screener_type": screener_type,
            "top_stock": {
                **top_stock,
                "news": [n.model_dump() for n in news_list]
            }
        }
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.error(f"화제 종목 조회 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"주식 조회 중 오류 발생: {str(e)}")


@router.get("/search", tags=["Stock Search"])
async def search_stocks(query: str = Query(..., description="검색 쿼리")):
    """주식 종목 검색"""
    return {
        "message": "주식 검색",
        "query": query,
        "results": []
    }


@router.get("/{ticker}", tags=["Stock Info"])
async def get_stock_info(ticker: str):
    """
    특정 종목의 상세 정보 조회 (종목 정보 + 관련 뉴스)
    
    Parameters:
    - ticker: 종목 코드 (예: AAPL, MSFT, NVDA)
    
    Returns:
    - 종목의 기본정보, 가격정보, 거래정보 + 관련 뉴스
    """
    try:
        if not ticker or not isinstance(ticker, str) or len(ticker.strip()) == 0:
            raise HTTPException(status_code=400, detail="유효한 종목 코드를 입력하세요.")
        
        # 종목 상세 정보 조회
        stock_result = await stock_service.get_stock_info(ticker)
        
        if stock_result.get("status") == "error":
            raise HTTPException(status_code=400, detail=stock_result.get("error", "종목 정보 조회 실패"))
        
        # 관련 뉴스 조회 (5개)
        news_result = await news_service.search_stock_news(ticker, limit=5)
        news_list = []
        
        if news_result.get("status") == "success":
            for news in news_result.get("news", []):
                try:
                    # published_date를 datetime으로 변환
                    pub_date = news.get("published_date", "")
                    if isinstance(pub_date, str) and pub_date:
                        try:
                            published_at = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                        except ValueError:
                            published_at = datetime.now()
                    else:
                        published_at = datetime.now()
                    
                    news_item = NewsItem(
                        title=news.get("title", ""),
                        summary=news.get("summary", ""),
                        source="Exa",
                        url=news.get("url", ""),
                        published_at=published_at,
                        related_tickers=[ticker]
                    )
                    news_list.append(news_item)
                except (KeyError, ValueError, TypeError) as e:
                    # 개별 뉴스 파싱 오류 무시
                    pass
        
        # 통합 응답 구성 (stock_result를 기반으로 news 추가)
        response = {
            **stock_result,
            "news": [n.model_dump() for n in news_list]
        }
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.error(f"종목 정보 조회 중 오류 ({ticker}): {str(e)}")
        raise HTTPException(status_code=500, detail=f"종목 조회 중 오류 발생: {str(e)}")
