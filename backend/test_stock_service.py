"""
주식 서비스 테스트
stock_service.py의 기능 검증
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.stock_service import StockService


async def test_get_trending_stocks():
    """화제 종목 조회 테스트"""
    print("\n" + "="*60)
    print("테스트 1: 화제 종목 조회 (most_actives)")
    print("="*60)
    
    service = StockService()
    
    # 테스트 1-1: 가장 거래량이 많은 종목
    result = await service.get_trending_stocks("most_actives")
    print(f"\n[Result] Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        top_stock = result.get('top_stock')
        if top_stock and top_stock.get('ticker'):
            print(f"✅ TOP 1 종목: {top_stock.get('ticker')}")
            print(f"   회사명: {top_stock.get('basic_info', {}).get('name')}")
            print(f"   현재가: {top_stock.get('price_info', {}).get('current_price')}")
            print(f"   거래량: {top_stock.get('trading_info', {}).get('volume')}")
        else:
            print("❌ 종목 정보를 찾을 수 없습니다.")
    else:
        print(f"❌ 오류: {result.get('message')}")


async def test_get_trending_stocks_gainers():
    """당일 상승 종목 조회 테스트"""
    print("\n" + "="*60)
    print("테스트 2: 화제 종목 조회 (day_gainers)")
    print("="*60)
    
    service = StockService()
    result = await service.get_trending_stocks("day_gainers")
    print(f"\n[Result] Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        top_stock = result.get('top_stock')
        if top_stock and top_stock.get('ticker'):
            print(f"✅ TOP 1 종목: {top_stock.get('ticker')}")
            print(f"   회사명: {top_stock.get('basic_info', {}).get('name')}")
            print(f"   현재가: {top_stock.get('price_info', {}).get('current_price')}")
        else:
            print("❌ 종목 정보를 찾을 수 없습니다.")
    else:
        print(f"❌ 오류: {result.get('message')}")


async def test_get_trending_stocks_losers():
    """당일 하락 종목 조회 테스트"""
    print("\n" + "="*60)
    print("테스트 3: 화제 종목 조회 (day_losers)")
    print("="*60)
    
    service = StockService()
    result = await service.get_trending_stocks("day_losers")
    print(f"\n[Result] Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        top_stock = result.get('top_stock')
        if top_stock and top_stock.get('ticker'):
            print(f"✅ TOP 1 종목: {top_stock.get('ticker')}")
            print(f"   회사명: {top_stock.get('basic_info', {}).get('name')}")
            print(f"   현재가: {top_stock.get('price_info', {}).get('current_price')}")
        else:
            print("❌ 종목 정보를 찾을 수 없습니다.")
    else:
        print(f"❌ 오류: {result.get('message')}")


async def test_get_stock_info():
    """종목 상세 정보 조회 테스트"""
    print("\n" + "="*60)
    print("테스트 4: 종목 상세 정보 조회 (AAPL)")
    print("="*60)
    
    service = StockService()
    result = await service.get_stock_info("AAPL")
    
    if result.get('status') != 'error':
        print(f"\n✅ 종목: {result.get('ticker')}")
        print(f"   회사명: {result.get('basic_info', {}).get('name')}")
        print(f"   섹터: {result.get('basic_info', {}).get('sector')}")
        print(f"   현재가: {result.get('price_info', {}).get('current_price')}")
        print(f"   거래량: {result.get('trading_info', {}).get('volume')}")
    else:
        print(f"❌ 오류: {result.get('error')}")


async def test_invalid_screener_type():
    """유효하지 않은 스크리너 타입 테스트"""
    print("\n" + "="*60)
    print("테스트 5: 유효하지 않은 스크리너 타입 처리")
    print("="*60)
    
    service = StockService()
    result = await service.get_trending_stocks("invalid_type")
    
    if result.get('status') == 'error':
        print(f"\n✅ 에러 처리 성공: {result.get('message')}")
    else:
        print(f"❌ 에러 처리 실패")


async def run_all_tests():
    """모든 테스트 실행"""
    print("\n" + "🧪 Stock Service 테스트 시작 ".center(60, "="))
    
    try:
        await test_get_trending_stocks()
        await test_get_trending_stocks_gainers()
        await test_get_trending_stocks_losers()
        await test_get_stock_info()
        await test_invalid_screener_type()
        
        print("\n" + "="*60)
        print("✅ 모든 테스트 완료!")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_all_tests())
