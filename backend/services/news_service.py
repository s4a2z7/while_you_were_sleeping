"""
뉴스 수집 서비스
Exa API를 사용한 뉴스 검색 및 수집
"""

from typing import List, Dict, Any, Optional
from exa_py import Exa
import logging
from datetime import datetime, timedelta
import os

# 로거 설정
logger = logging.getLogger(__name__)


class NewsService:
    """뉴스 데이터 관련 비즈니스 로직"""
    
    def __init__(self):
        """NewsService 초기화"""
        # Exa API 키 설정
        api_key = os.getenv("EXA_API_KEY")
        if not api_key:
            logger.warning("EXA_API_KEY 환경 변수가 설정되지 않았습니다.")
            self.client = None
        else:
            self.client = Exa(api_key=api_key)
    
    async def search_stock_news(self, ticker: str, limit: int = 5) -> Dict[str, Any]:
        """
        주식 관련 뉴스 검색
        
        Args:
            ticker: 종목 코드 (예: "AAPL", "MSFT")
            limit: 결과 개수 (기본값: 5)
        
        Returns:
            검색된 뉴스 목록
        """
        try:
            if not ticker or not isinstance(ticker, str):
                raise ValueError(f"유효하지 않은 티커: {ticker}")
            
            if not self.client:
                logger.error("Exa API 클라이언트가 초기화되지 않았습니다.")
                return {
                    "status": "error",
                    "error_type": "api_not_initialized",
                    "message": "Exa API가 초기화되지 않았습니다. EXA_API_KEY를 설정해주세요.",
                    "data": None
                }
            
            ticker = ticker.upper().strip()
            logger.info(f"주식 뉴스 검색 시작: {ticker}")
            
            # 검색 키워드 설정
            query = f"{ticker} stock news"
            
            # 최근 24시간 기준 설정
            start_published_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
            
            logger.info(f"검색 쿼리: {query}, 기간: {start_published_date}~현재")
            
            # Exa API를 사용하여 뉴스 검색
            # search() 메서드 사용
            results = self.client.search(
                query=query,
                num_results=limit,
                start_published_date=start_published_date
            )
            
            # 결과가 없을 경우 처리
            if not results or not hasattr(results, 'results') or len(results.results) == 0:
                logger.warning(f"검색 결과 없음: {ticker}")
                return {
                    "status": "empty",
                    "message": f"{ticker}에 대한 뉴스 검색 결과가 없습니다.",
                    "data": []
                }
            
            # 검색 결과 파싱
            news_list = []
            for item in results.results:
                news_item = {
                    "title": item.title,
                    "url": item.url,
                    "published_date": item.published_date if hasattr(item, 'published_date') else "N/A",
                    "summary": item.text if hasattr(item, 'text') else "N/A",
                }
                news_list.append(news_item)
            
            logger.info(f"뉴스 검색 완료: {ticker} ({len(news_list)}개)")
            
            return {
                "status": "success",
                "ticker": ticker,
                "query": query,
                "count": len(news_list),
                "news": news_list
            }
        
        except ValueError as e:
            logger.error(f"입력값 오류: {str(e)}")
            return {
                "status": "error",
                "error_type": "validation_error",
                "message": str(e),
                "data": None
            }
        except Exception as e:
            logger.error(f"뉴스 검색 중 오류: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "message": str(e),
                "data": None
            }
    
    async def get_market_news(self, limit: int = 10) -> Dict[str, Any]:
        """
        시장 관련 뉴스 조회
        
        Args:
            limit: 결과 개수
        
        Returns:
            시장 뉴스 목록
        """
        try:
            if not self.client:
                logger.error("Exa API 클라이언트가 초기화되지 않았습니다.")
                return {
                    "status": "error",
                    "message": "Exa API가 초기화되지 않았습니다.",
                    "data": None
                }
            
            logger.info("시장 뉴스 조회 시작")
            
            # 시장 관련 뉴스 검색
            query = "stock market news"
            start_published_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
            
            results = self.client.search(
                query=query,
                num_results=limit,
                start_published_date=start_published_date
            )
            
            if not results or not hasattr(results, 'results') or len(results.results) == 0:
                logger.warning("시장 뉴스 검색 결과 없음")
                return {
                    "status": "empty",
                    "message": "시장 뉴스 검색 결과가 없습니다.",
                    "data": []
                }
            
            news_list = []
            for item in results.results:
                news_item = {
                    "title": item.title,
                    "url": item.url,
                    "published_date": item.published_date if hasattr(item, 'published_date') else "N/A",
                    "summary": item.text if hasattr(item, 'text') else "N/A",
                }
                news_list.append(news_item)
            
            logger.info(f"시장 뉴스 조회 완료 ({len(news_list)}개)")
            
            return {
                "status": "success",
                "query": query,
                "count": len(news_list),
                "news": news_list
            }
        
        except Exception as e:
            logger.error(f"시장 뉴스 조회 중 오류: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    async def get_stock_news(self, ticker: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        특정 종목 관련 뉴스 조회
        
        Args:
            ticker: 종목 심볼
            limit: 결과 개수
        
        Returns:
            종목 뉴스 목록 (리스트 형식)
        """
        try:
            # EXA API 키가 없으면 빈 배열 반환
            if not self.client:
                logger.warning(f"EXA API 클라이언트 없음. {ticker}의 뉴스를 조회할 수 없습니다.")
                return []
            
            if not ticker or not isinstance(ticker, str):
                logger.error(f"유효하지 않은 티커: {ticker}")
                return []
            
            result = await self.search_stock_news(ticker, limit)
            
            # 성공 시 뉴스 리스트 반환
            if result.get("status") == "success" and "news" in result:
                news_list = result.get("news", [])
                # 형식 정규화
                formatted_news = []
                for news in news_list:
                    try:
                        formatted_news.append({
                            "title": news.get("title", ""),
                            "summary": news.get("summary", ""),
                            "source": news.get("source", "Exa"),
                            "url": news.get("url", ""),
                            "published_at": news.get("published_date", "")
                        })
                    except (TypeError, AttributeError) as e:
                        logger.warning(f"뉴스 항목 파싱 실패: {e}")
                        continue
                return formatted_news
            
            # 결과가 없거나 실패 시 빈 배열 반환
            logger.debug(f"{ticker}의 뉴스 조회 결과: {result.get('status')}")
            return []
            
        except Exception as e:
            logger.error(f"종목 뉴스 조회 중 오류 ({ticker}): {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return []
