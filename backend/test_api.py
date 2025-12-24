"""
API 엔드포인트 테스트
"""

import asyncio
import sys
from pathlib import Path

# 부모 디렉토리를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from api.stocks import get_trending_stocks, get_stock_info


async def test_trending_stocks():
    """화제 종목 조회 테스트"""
    print("\n=== GET /api/stocks/trending 테스트 ===")
    try:
        result = await get_trending_stocks("most_actives")
        print("✓ most_actives 조회 성공")
        print(f"  - 상태: {result.get('status')}")
        top_stock = result.get('top_stock', {})
        print(f"  - 종목: {top_stock.get('ticker')}")
        print(f"  - 뉴스: {len(top_stock.get('news', []))}개")
        return True
    except Exception as e:
        print(f"✗ 에러: {type(e).__name__}")
        print(f"  - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_stock_info():
    """종목 상세 정보 조회 테스트"""
    print("\n=== GET /api/stocks/{ticker} 테스트 ===")
    try:
        result = await get_stock_info("AAPL")
        print("✓ AAPL 조회 성공")
        print(f"  - 상태: {result.get('status')}")
        print(f"  - 종목: {result.get('ticker', 'N/A')}")
        print(f"  - 뉴스: {len(result.get('news', []))}개")
        return True
    except Exception as e:
        print(f"✗ 에러: {type(e).__name__}")
        print(f"  - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    print("화제 종목 조회 API 테스트 시작...")
    
    result1 = await test_trending_stocks()
    result2 = await test_stock_info()
    
    print("\n=== 테스트 결과 ===")
    print(f"trending API: {'✓ 성공' if result1 else '✗ 실패'}")
    print(f"stock info API: {'✓ 성공' if result2 else '✗ 실패'}")


if __name__ == "__main__":
    asyncio.run(main())
