"""
브리핑 생성 서비스
브리핑 데이터 수집, 분석, 요약
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .stock_service import StockService
from .news_service import NewsService
import logging

# 로거 설정
logger = logging.getLogger(__name__)


class BriefingService:
    """브리핑 생성 관련 비즈니스 로직"""
    
    def __init__(self):
        self.stock_service = StockService()
        self.news_service = NewsService()
    
    async def generate_briefing_content(
        self,
        ticker: str,
        screener_type: str = "most_actives"
    ) -> str:
        """
        종목 기반 브리핑 마크다운 콘텐츠 생성
        
        Args:
            ticker: 종목 코드 (예: "TSLA")
            screener_type: 스크리너 유형 ("most_actives", "day_gainers", "day_losers")
        
        Returns:
            브리핑 마크다운 텍스트
        """
        try:
            # 입력값 검증
            if not ticker or not isinstance(ticker, str):
                raise ValueError(f"유효하지 않은 티커: {ticker}")
            
            ticker = ticker.upper().strip()
            
            # 유효한 screener_type 확인
            valid_types = {"most_actives", "day_gainers", "day_losers"}
            if screener_type not in valid_types:
                raise ValueError(f"유효하지 않은 screener_type: {screener_type}")
            
            logger.info(f"브리핑 생성 시작: {ticker} (screener_type: {screener_type})")
            
            # 1. 종목 정보 조회
            stock_info = await self.stock_service.get_stock_info(ticker)
            
            if stock_info.get("status") == "error":
                logger.error(f"종목 정보 조회 실패: {ticker} - {stock_info.get('error')}")
                raise ValueError(f"{ticker} 종목 정보를 조회할 수 없습니다.")
            
            # 2. 뉴스 조회
            news_items_list = await self.news_service.get_stock_news(ticker)
            
            logger.debug(f"뉴스 조회 완료: {ticker} ({len(news_items_list)}개)")
            
            # 3. 마크다운 포맷 생성
            briefing_md = self._format_briefing_markdown(
                ticker=ticker,
                stock_info=stock_info,
                news_items=news_items_list,
                screener_type=screener_type
            )
            
            logger.info(f"브리핑 생성 완료: {ticker}")
            return briefing_md
            
        except ValueError as e:
            logger.error(f"입력값 오류: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"브리핑 생성 중 오류 ({ticker}): {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise
    
    def _format_briefing_markdown(
        self,
        ticker: str,
        stock_info: Dict[str, Any],
        news_items: List[Dict[str, Any]],
        screener_type: str
    ) -> str:
        """마크다운 포맷 브리핑 생성"""
        
        # 기본 정보 추출
        name = stock_info.get("name", "Unknown")
        price = stock_info.get("price", 0)
        change_percent = stock_info.get("change_percent", 0)
        volume = stock_info.get("volume", 0)
        market_cap = stock_info.get("market_cap", "N/A")
        sector = stock_info.get("sector", "N/A")
        industry = stock_info.get("industry", "N/A")
        pe_ratio = stock_info.get("pe_ratio", "N/A")
        
        # 날짜 포맷
        now = datetime.now()
        date_str = now.strftime("%Y년 %m월 %d일 %H:%M:%S")
        
        # 변동률 텍스트
        change_text = "상승" if change_percent >= 0 else "하락"
        change_sign = "+" if change_percent >= 0 else ""
        
        # 마크다운 생성
        md = f"""# {ticker} - {name} 브리핑

**생성 시간**: {date_str}  
**분류**: {screener_type}

---

## 📊 종목 정보

| 항목 | 값 |
|------|-----|
| 티커 | {ticker} |
| 회사명 | {name} |
| 현재 가격 | ${price:.2f} |
| 변동률 | {change_sign}{change_percent:.2f}% ({change_text}) |
| 거래량 | {self._format_volume(volume)} |
| 시가총액 | {market_cap} |
| 섹터 | {sector} |
| 산업 | {industry} |
| PER | {pe_ratio} |

---

## 📰 관련 뉴스

"""
        
        if news_items:
            for i, news in enumerate(news_items[:5], 1):  # 최대 5개 뉴스
                title = news.get("title", "제목 없음")
                summary = news.get("summary", "")
                source = news.get("source", "Unknown Source")
                url = news.get("url", "#")
                published_at = news.get("published_at", "")
                
                md += f"""### {i}. {title}

**출처**: {source}  
**시간**: {published_at}  
**요약**: {summary}

[원문 보기]({url})

"""
        else:
            md += "현재 관련 뉴스가 없습니다.\n\n"
        
        # 요약 섹션
        md += f"""---

## 💡 분석 요약

{name}({ticker})은 {screener_type} 스크리너에서 선정된 종목입니다.

- **가격 동향**: ${price:.2f}에서 {change_sign}{change_percent:.2f}% {change_text}
- **거래 활동**: 거래량 {self._format_volume(volume)}
- **기본 정보**: {sector} 섹터, {industry} 산업
- **밸류에이션**: PER {pe_ratio}

이 브리핑은 실시간 시장 데이터를 기반으로 자동 생성되었습니다.

---

*자동 생성: While You Were Sleeping Dashboard*
"""
        
        return md
    
    @staticmethod
    def _format_volume(volume: int) -> str:
        """거래량을 사람이 읽을 수 있는 형식으로 변환"""
        if volume >= 1_000_000:
            return f"{volume / 1_000_000:.1f}M"
        elif volume >= 1_000:
            return f"{volume / 1_000:.1f}K"
        return str(volume)
    
    async def generate_daily_briefing(self) -> Dict[str, Any]:
        """일일 브리핑 생성"""
        try:
            # TODO: 브리핑 생성 로직 구현
            # 1. 트렌딩 종목 수집
            # 2. 뉴스 수집
            # 3. AI 분석 및 요약
            return {
                "date": None,
                "briefing": None,
                "stocks": [],
                "news": []
            }
        except Exception as e:
            print(f"브리핑 생성 중 오류: {str(e)}")
            raise
    
    async def analyze_stocks(self, stocks: List[str]) -> Dict[str, Any]:
        """종목 분석"""
        try:
            # TODO: 종목 분석 로직 구현
            return {"analysis": None}
        except Exception as e:
            print(f"종목 분석 중 오류: {str(e)}")
            raise
    
    async def summarize_news(self, news: List[Dict[str, Any]]) -> str:
        """뉴스 요약"""
        try:
            # TODO: Gemini API를 사용한 뉴스 요약 구현
            return ""
        except Exception as e:
            print(f"뉴스 요약 중 오류: {str(e)}")
            raise
