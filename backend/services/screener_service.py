"""
화제 종목 스크리닝 서비스
화제 종목을 조회하고 저장하는 스크립트
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
import json
import sys

# 부모 디렉토리를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.stock_service import StockService

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_screener():
    """화제 종목 조회 실행"""
    try:
        logger.info("=" * 50)
        logger.info("화제 종목 스크리닝 시작")
        logger.info("=" * 50)
        
        service = StockService()
        
        # 3가지 스크리너 타입 조회
        screener_types = ["most_actives", "day_gainers", "day_losers"]
        results = {}
        
        for screener_type in screener_types:
            logger.info(f"\n[{screener_type.upper()}] 조회 중...")
            
            result = await service.get_trending_stocks(screener_type)
            
            if result.get("status") == "success":
                top_stock = result.get("top_stock", {})
                logger.info(f"✅ 성공: {top_stock.get('ticker')} - {top_stock.get('name')}")
                logger.info(f"   가격: ${top_stock.get('price'):.2f}")
                logger.info(f"   변동률: {top_stock.get('change_percent'):.2f}%")
                logger.info(f"   거래량: {top_stock.get('volume'):,}")
                results[screener_type] = result
            else:
                logger.error(f"❌ 실패: {result.get('message')}")
                results[screener_type] = result
        
        # 결과를 JSON 파일로 저장
        output_dir = Path(__file__).parent.parent / "output" / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"screener_results_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"\n✅ 결과 저장: {output_file}")
        logger.info("=" * 50)
        logger.info("화제 종목 스크리닝 완료")
        logger.info("=" * 50)
        
        return results
        
    except Exception as e:
        logger.error(f"❌ 스크리닝 중 오류: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    try:
        asyncio.run(run_screener())
    except KeyboardInterrupt:
        logger.info("사용자에 의해 중단됨")
    except Exception as e:
        logger.error(f"치명적 오류: {str(e)}")
        sys.exit(1)
