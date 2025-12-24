"""
주식 데이터 수집 서비스
yahooquery를 사용한 주식 정보 조회
"""

from typing import List, Dict, Any, Optional, Literal
from yahooquery import Screener, Ticker
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# 스크리너 타입 리터럴
ScreenerType = Literal["most_actives", "day_gainers", "day_losers"]


class StockService:
    """주식 데이터 관련 비즈니스 로직"""
    
    def __init__(self):
        """StockService 초기화"""
        self.screener = Screener()
    
    async def get_trending_stocks(self, screener_type: ScreenerType = "most_actives") -> Dict[str, Any]:
        """
        화제 종목 조회 (트렌딩 중인 주식 종목)
        
        Args:
            screener_type: 스크리너 타입
                - "most_actives": 가장 거래량이 많은 종목
                - "day_gainers": 당일 가장 많이 오른 종목
                - "day_losers": 당일 가장 많이 내린 종목
        
        Returns:
            선정된 TOP 1 종목의 상세 정보
        """
        try:
            # 유효한 스크리너 타입 확인
            valid_types = {"most_actives", "day_gainers", "day_losers"}
            if screener_type not in valid_types:
                raise ValueError(f"유효하지 않은 스크리너 타입: {screener_type}. 허용값: {valid_types}")
            
            logger.info(f"화제 종목 조회 시작 (타입: {screener_type})")
            
            # Screener를 사용하여 종목 목록 조회
            # get_screeners()는 {screener_name: {데이터}}  형태의 dict 반환
            screened_result = self.screener.get_screeners(screener_type)
            
            # 결과 파싱
            if screened_result is None:
                logger.warning(f"스크리너 결과 없음: {screener_type}")
                return {
                    "status": "empty",
                    "message": f"{screener_type}에 대한 결과가 없습니다.",
                    "data": None
                }
            
            # screened_result[screener_type] 에서 quotes 추출
            screened_data = screened_result.get(screener_type, {})
            quotes = screened_data.get('quotes', [])
            
            if not quotes or len(quotes) == 0:
                logger.warning(f"스크리너 결과 없음: {screener_type}")
                return {
                    "status": "empty",
                    "message": f"{screener_type}에 대한 결과가 없습니다.",
                    "data": None
                }
            
            # 첫 번째 종목 (TOP 1) 선정
            top_stock_data = quotes[0]
            ticker_symbol = top_stock_data.get('symbol')
            
            if not ticker_symbol:
                raise ValueError("종목 심볼을 찾을 수 없습니다.")
            
            logger.info(f"TOP 1 종목 선정: {ticker_symbol}")
            
            # 선정된 종목의 상세 정보 조회
            stock_detail = await self.get_stock_info(ticker_symbol)
            
            return {
                "status": "success",
                "screener_type": screener_type,
                "top_stock": stock_detail
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
            logger.error(f"화제 종목 조회 중 오류: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "message": str(e),
                "data": None
            }
    
    async def get_stock_info(self, ticker: str) -> Dict[str, Any]:
        """
        특정 종목의 상세 정보 조회
        
        Args:
            ticker: 종목 심볼 (예: "AAPL", "MSFT")
        
        Returns:
            종목의 상세 정보 (프론트엔드 호환 형식)
        """
        try:
            if not ticker or not isinstance(ticker, str):
                raise ValueError(f"유효하지 않은 티커: {ticker}")
            
            ticker = ticker.upper().strip()
            logger.info(f"종목 정보 조회: {ticker}")
            
            # yahooquery Ticker를 사용하여 종목 정보 조회
            stock = Ticker(ticker)
            
            # 기본값 설정
            name = "N/A"
            sector = "N/A"
            industry = "N/A"
            price = 0
            previous_close = 0
            day_high = 0
            day_low = 0
            week_52_high = 0
            week_52_low = 0
            volume = 0
            avg_volume = 0
            market_cap = "N/A"
            pe_ratio = "N/A"
            
            # asset_profile에서 기본 정보
            try:
                asset_profile_data = stock.asset_profile
                if isinstance(asset_profile_data, dict):
                    profile = asset_profile_data.get(ticker, {})
                    if isinstance(profile, dict):
                        name = profile.get("longName", profile.get("website", "N/A"))
                        sector = profile.get("sector", "N/A")
                        industry = profile.get("industry", "N/A")
            except Exception as e:
                logger.warning(f"asset_profile 로드 실패 ({ticker}): {e}")
            
            # summary_detail에서 가격 정보
            try:
                summary_data = stock.summary_detail
                if isinstance(summary_data, dict) and ticker in summary_data:
                    summary = summary_data[ticker]
                    # 현재가 구하기 (regularMarketPrice가 없으면 bid/ask 평균 또는 open 사용)
                    if "regularMarketPrice" in summary and summary["regularMarketPrice"] and summary["regularMarketPrice"] > 0:
                        price = summary["regularMarketPrice"]
                        logger.debug(f"가격 source: regularMarketPrice ({ticker})")
                    elif "bid" in summary and "ask" in summary and summary.get("bid", 0) > 0 and summary.get("ask", 0) > 0:
                        price = (summary["bid"] + summary["ask"]) / 2
                        logger.debug(f"가격 source: bid/ask average ({ticker})")
                    elif "regularMarketOpen" in summary and summary["regularMarketOpen"] and summary["regularMarketOpen"] > 0:
                        price = summary["regularMarketOpen"]
                        logger.debug(f"가격 source: regularMarketOpen ({ticker})")
                    else:
                        logger.warning(f"유효한 가격 정보를 찾을 수 없습니다 ({ticker})")
                    
                    previous_close = summary.get("regularMarketPreviousClose", 0) or 0
                    day_high = summary.get("regularMarketDayHigh", 0) or 0
                    day_low = summary.get("regularMarketDayLow", 0) or 0
                    week_52_high = summary.get("fiftyTwoWeekHigh", 0) or 0
                    week_52_low = summary.get("fiftyTwoWeekLow", 0) or 0
                    volume = summary.get("regularMarketVolume", 0) or 0
                    avg_volume = summary.get("averageVolume", 0) or 0
                    market_cap_value = summary.get("marketCap", 0)
                    if market_cap_value and market_cap_value > 0:
                        if market_cap_value >= 1e12:
                            market_cap = f"${market_cap_value / 1e12:.1f}T"
                        elif market_cap_value >= 1e9:
                            market_cap = f"${market_cap_value / 1e9:.1f}B"
                        else:
                            market_cap = f"${market_cap_value / 1e6:.1f}M"
                    pe_ratio_value = summary.get("trailingPE")
                    if pe_ratio_value:
                        pe_ratio = f"{pe_ratio_value:.2f}"
            except Exception as e:
                logger.warning(f"summary_detail 로드 실패 ({ticker}): {e}")
            
            # change_percent 계산 (0으로 나누기 방지)
            change_percent = 0
            if previous_close and previous_close > 0 and price:
                change_percent = ((price - previous_close) / previous_close) * 100
            elif previous_close == 0 and price > 0:
                logger.warning(f"previous_close가 0입니다 ({ticker}). change_percent를 계산할 수 없습니다.")
                change_percent = 0
            
            logger.info(f"종목 정보 조회 완료: {ticker}")
            
            # 프론트엔드 호환 형식으로 반환
            return {
                "ticker": ticker,
                "name": name,
                "price": price,
                "change_percent": change_percent,
                "volume": volume,
                "market_cap": market_cap,
                "sector": sector,
                "industry": industry,
                "pe_ratio": pe_ratio,
                "status": "success"
            }
        
        except Exception as e:
            logger.error(f"종목 정보 조회 중 오류 ({ticker}): {str(e)}")
            return {
                "ticker": ticker,
                "error": str(e),
                "status": "error"
            }
    
    async def screen_stocks(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        조건에 맞는 종목 스크리닝
        
        Args:
            criteria: 스크리닝 조건
        
        Returns:
            조건에 맞는 종목 목록
        """
        try:
            logger.info(f"종목 스크리닝 시작: {criteria}")
            
            # TODO: 커스텀 스크리닝 로직 구현
            # 현재는 기본 스크리닝만 지원
            return []
        
        except Exception as e:
            logger.error(f"종목 스크리닝 중 오류: {str(e)}")
            return []
