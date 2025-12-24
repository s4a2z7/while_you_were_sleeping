"""
데이터 모델 정의
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class StockInfo(BaseModel):
    """주식 정보 모델"""
    ticker: str = Field(..., description="종목 코드")
    name: str = Field(..., description="회사명")
    price: float = Field(..., description="현재 가격")
    change_percent: float = Field(..., description="변동률 (%)")
    volume: int = Field(..., description="거래량")


class NewsItem(BaseModel):
    """뉴스 항목 모델"""
    title: str = Field(..., description="제목")
    summary: str = Field(..., description="요약")
    source: str = Field(..., description="출처")
    url: str = Field(..., description="URL")
    published_at: datetime = Field(..., description="발행 시간")
    related_tickers: List[str] = Field(default_factory=list, description="관련 종목")


class BriefingContent(BaseModel):
    """브리핑 내용 모델"""
    title: str = Field(..., description="제목")
    summary: str = Field(..., description="요약")
    trending_stocks: List[StockInfo] = Field(..., description="트렌딩 종목")
    news_highlights: List[NewsItem] = Field(..., description="주요 뉴스")


class Briefing(BaseModel):
    """브리핑 모델"""
    date: datetime = Field(..., description="브리핑 날짜")
    content: BriefingContent = Field(..., description="브리핑 내용")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
    
    class Config:
        from_attributes = True


class TrendingStockDetail(BaseModel):
    """화제 종목 상세 정보 (뉴스 포함)"""
    ticker: str = Field(..., description="종목 코드")
    name: str = Field(..., description="회사명")
    price: float = Field(..., description="현재 가격")
    change_percent: float = Field(..., description="변동률 (%)")
    volume: int = Field(..., description="거래량")
    market_cap: Optional[str] = Field(None, description="시가총액")
    sector: Optional[str] = Field(None, description="섹터")
    industry: Optional[str] = Field(None, description="산업")
    pe_ratio: Optional[str] = Field(None, description="PER")
    news: List[NewsItem] = Field(default_factory=list, description="관련 뉴스")


class StockDetailResponse(BaseModel):
    """종목 상세 정보 응답 (뉴스 포함)"""
    ticker: str = Field(..., description="종목 코드")
    name: str = Field(..., description="회사명")
    price: float = Field(..., description="현재 가격")
    change_percent: float = Field(..., description="변동률 (%)")
    volume: int = Field(..., description="거래량")
    market_cap: Optional[str] = Field(None, description="시가총액")
    sector: Optional[str] = Field(None, description="섹터")
    industry: Optional[str] = Field(None, description="산업")
    pe_ratio: Optional[str] = Field(None, description="PER")
    news: List[NewsItem] = Field(default_factory=list, description="관련 뉴스")
