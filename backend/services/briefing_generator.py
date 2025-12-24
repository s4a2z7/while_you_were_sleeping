"""
브리핑 생성 자동화 서비스
화제 종목 기반 브리핑을 생성하고 저장하는 스크립트
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
from services.briefing_service import BriefingService

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def generate_briefings():
    """브리핑 생성 및 저장"""
    try:
        logger.info("=" * 50)
        logger.info("브리핑 생성 시작")
        logger.info("=" * 50)
        
        stock_service = StockService()
        briefing_service = BriefingService()
        
        # 3가지 스크리너 타입별 브리핑 생성
        screener_types = ["most_actives", "day_gainers", "day_losers"]
        briefings = {}
        
        for screener_type in screener_types:
            logger.info(f"\n[{screener_type.upper()}] 브리핑 생성 중...")
            
            try:
                # 화제 종목 조회
                stock_result = await stock_service.get_trending_stocks(screener_type)
                
                if stock_result.get("status") != "success":
                    logger.error(f"❌ 종목 조회 실패: {stock_result.get('message')}")
                    continue
                
                top_stock = stock_result.get("top_stock", {})
                ticker = top_stock.get("ticker")
                
                logger.info(f"   종목: {ticker}")
                
                # 브리핑 콘텐츠 생성
                briefing_content = await briefing_service.generate_briefing_content(
                    ticker=ticker,
                    screener_type=screener_type
                )
                
                briefings[screener_type] = {
                    "ticker": ticker,
                    "screener_type": screener_type,
                    "generated_at": datetime.now().isoformat(),
                    "content": briefing_content,
                    "top_stock": top_stock
                }
                
                logger.info(f"✅ 완료: {ticker} 브리핑 생성됨")
                
            except Exception as e:
                logger.error(f"❌ {screener_type} 브리핑 생성 실패: {str(e)}")
                briefings[screener_type] = {
                    "screener_type": screener_type,
                    "status": "error",
                    "error": str(e)
                }
        
        # 결과를 JSON 파일로 저장
        output_dir = Path(__file__).parent.parent / "output" / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"briefings_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(briefings, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"\n✅ 브리핑 저장: {output_file}")
        
        # 마크다운 형식으로도 저장
        md_file = output_dir.parent / "reports" / f"briefing_{datetime.now().strftime('%Y%m%d')}.md"
        md_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# 당신이 잠든 사이 - 일일 브리핑\n\n")
            f.write(f"생성 일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}\n\n")
            
            for screener_type, briefing in briefings.items():
                if "error" not in briefing:
                    f.write(f"## {briefing.get('screener_type', '').upper()}\n\n")
                    f.write(f"**종목**: {briefing.get('ticker')}\n\n")
                    f.write(briefing.get('content', '') + "\n\n---\n\n")
        
        logger.info(f"✅ 마크다운 저장: {md_file}")
        logger.info("=" * 50)
        logger.info("브리핑 생성 완료")
        logger.info("=" * 50)
        
        return briefings
        
    except Exception as e:
        logger.error(f"❌ 브리핑 생성 중 오류: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    try:
        asyncio.run(generate_briefings())
    except KeyboardInterrupt:
        logger.info("사용자에 의해 중단됨")
    except Exception as e:
        logger.error(f"치명적 오류: {str(e)}")
        sys.exit(1)
