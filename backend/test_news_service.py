"""
뉴스 서비스 테스트
news_service.py의 기능 검증
"""

import asyncio
import sys
import os
from pathlib import Path

# 환경 변수 설정 (테스트용 임시 키)
# 실제 API 키는 .env 파일에서 로드되어야 함
os.environ["EXA_API_KEY"] = os.getenv("EXA_API_KEY", "test_key")

# 프로젝트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.news_service import NewsService


async def test_search_stock_news():
    """주식 뉴스 검색 테스트"""
    print("\n" + "="*60)
    print("테스트 1: 주식 뉴스 검색 (AAPL)")
    print("="*60)
    
    service = NewsService()
    
    # API 키가 없는 경우 처리
    if not os.getenv("EXA_API_KEY") or os.getenv("EXA_API_KEY") == "test_key":
        print("⚠️  경고: EXA_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일에 다음을 추가하세요:")
        print("   EXA_API_KEY=your_api_key_here")
        result = await service.search_stock_news("AAPL")
        print(f"\n[Result] Status: {result.get('status')}")
        print(f"Message: {result.get('message')}")
        return
    
    result = await service.search_stock_news("AAPL", limit=3)
    print(f"\n[Result] Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        print(f"Ticker: {result.get('ticker')}")
        print(f"Count: {result.get('count')}")
        news_list = result.get('news', [])
        for i, news in enumerate(news_list[:3], 1):
            print(f"\n  뉴스 {i}:")
            print(f"    제목: {news.get('title')[:60]}...")
            print(f"    URL: {news.get('url')}")
            print(f"    발행일: {news.get('published_date')}")
    else:
        print(f"❌ 오류: {result.get('message')}")


async def test_search_different_tickers():
    """다른 종목 뉴스 검색 테스트"""
    print("\n" + "="*60)
    print("테스트 2: 다양한 종목 뉴스 검색")
    print("="*60)
    
    service = NewsService()
    
    if not os.getenv("EXA_API_KEY") or os.getenv("EXA_API_KEY") == "test_key":
        print("⚠️  API 키가 설정되지 않았습니다.")
        return
    
    tickers = ["NVDA", "MSFT", "GOOGL"]
    
    for ticker in tickers:
        result = await service.search_stock_news(ticker, limit=1)
        if result.get('status') == 'success':
            news_count = result.get('count', 0)
            print(f"\n✅ {ticker}: {news_count}개 뉴스 발견")
        else:
            print(f"\n❌ {ticker}: {result.get('message')}")


async def test_market_news():
    """시장 뉴스 조회 테스트"""
    print("\n" + "="*60)
    print("테스트 3: 시장 뉴스 조회")
    print("="*60)
    
    service = NewsService()
    
    if not os.getenv("EXA_API_KEY") or os.getenv("EXA_API_KEY") == "test_key":
        print("⚠️  API 키가 설정되지 않았습니다.")
        return
    
    result = await service.get_market_news(limit=3)
    print(f"\n[Result] Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        print(f"Count: {result.get('count')}")
        news_list = result.get('news', [])
        for i, news in enumerate(news_list[:2], 1):
            print(f"\n  뉴스 {i}: {news.get('title')[:50]}...")
    else:
        print(f"❌ 오류: {result.get('message')}")


async def test_invalid_ticker():
    """유효하지 않은 종목 테스트"""
    print("\n" + "="*60)
    print("테스트 4: 유효하지 않은 입력 처리")
    print("="*60)
    
    service = NewsService()
    
    result = await service.search_stock_news("")
    if result.get('status') == 'error':
        print(f"\n✅ 에러 처리 성공: {result.get('message')}")
    else:
        print(f"❌ 에러 처리 실패")


async def test_no_api_key():
    """API 키 없음 테스트"""
    print("\n" + "="*60)
    print("테스트 5: API 키 없음 처리")
    print("="*60)
    
    # 임시로 API 키 제거
    original_key = os.environ.get("EXA_API_KEY")
    os.environ.pop("EXA_API_KEY", None)
    
    service = NewsService()
    result = await service.search_stock_news("AAPL")
    
    if result.get('status') == 'error':
        print(f"\n✅ API 키 없음 처리 성공")
        print(f"   메시지: {result.get('message')}")
    else:
        print(f"❌ 처리 실패")
    
    # API 키 복구
    if original_key:
        os.environ["EXA_API_KEY"] = original_key


async def run_all_tests():
    """모든 테스트 실행"""
    print("\n" + "🧪 News Service 테스트 시작 ".center(60, "="))
    
    try:
        await test_search_stock_news()
        await test_search_different_tickers()
        await test_market_news()
        await test_invalid_ticker()
        await test_no_api_key()
        
        print("\n" + "="*60)
        print("✅ 모든 테스트 완료!")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_all_tests())
