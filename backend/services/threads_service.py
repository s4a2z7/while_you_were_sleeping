"""
Threads 자동 발행 서비스
생성된 브리핑 이미지를 Threads에 정기적으로 발행
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
import json
import os

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ThreadsService:
    """Threads 자동 발행 서비스"""
    
    def __init__(self):
        """Threads 서비스 초기화"""
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.client = None
        self.data_dir = Path(__file__).parent.parent / "output" / "data"
        self.image_dir = Path(__file__).parent.parent / "output" / "images"
        
        if not self.username or not self.password:
            logger.warning("⚠️  Threads 계정 정보가 설정되지 않았습니다.")
            logger.warning(f"    INSTAGRAM_USERNAME: {'✓' if self.username else '✗'}")
            logger.warning(f"    INSTAGRAM_PASSWORD: {'✓' if self.password else '✗'}")
            return
        
        try:
            from instagrapi import Client
            self.client = Client()
            logger.info("✓ Threads 클라이언트 초기화 완료")
        except ImportError:
            logger.error("❌ instagrapi가 설치되지 않았습니다.")
            logger.error("   pip install instagrapi 실행 후 재시도하세요.")
            self.client = None
        except Exception as e:
            logger.error(f"❌ Threads 클라이언트 초기화 실패: {e}")
            self.client = None
    
    def login(self) -> bool:
        """Threads 로그인"""
        try:
            if not self.client or not self.username or not self.password:
                logger.error("❌ Threads 설정이 불완전합니다.")
                return False
            
            logger.info(f"🔐 Threads 로그인 중 ({self.username})...")
            self.client.login(self.username, self.password)
            logger.info("✅ Threads 로그인 성공")
            return True
            
        except Exception as e:
            logger.error(f"❌ Threads 로그인 실패: {str(e)}")
            return False
    
    def get_latest_image(self):
        """가장 최신 브리핑 이미지 찾기"""
        try:
            if not self.image_dir.exists():
                logger.warning(f"⚠️  이미지 폴더가 없습니다: {self.image_dir}")
                return None
            
            image_files = list(self.image_dir.glob("briefing_card_*.png"))
            if not image_files:
                logger.warning("⚠️  브리핑 이미지를 찾을 수 없습니다.")
                return None
            
            latest_image = sorted(image_files)[-1]
            logger.info(f"✓ 최신 이미지 찾음: {latest_image.name}")
            return latest_image
            
        except Exception as e:
            logger.error(f"❌ 이미지 조회 오류: {e}")
            return None
    
    def get_latest_stock_data(self):
        """가장 최신 주식 데이터 조회"""
        try:
            if not self.data_dir.exists():
                logger.warning(f"⚠️  데이터 폴더가 없습니다: {self.data_dir}")
                return {}
            
            json_files = list(self.data_dir.glob("screener_results_*.json"))
            if not json_files:
                logger.warning("⚠️  스크리너 결과를 찾을 수 없습니다.")
                return {}
            
            latest_json = sorted(json_files)[-1]
            with open(latest_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"✓ 최신 데이터 로드: {latest_json.name}")
            return data
            
        except Exception as e:
            logger.error(f"❌ 데이터 조회 오류: {e}")
            return {}
    
    def post_image(self, image_path, caption: str) -> bool:
        """Threads에 이미지 업로드"""
        try:
            if not self.client:
                logger.error("❌ Threads 클라이언트가 초기화되지 않았습니다.")
                return False
            
            if not image_path.exists():
                logger.error(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
                return False
            
            logger.info(f"📸 Threads에 이미지 업로드 중: {image_path.name}")
            logger.info(f"📝 캡션: {caption[:100]}...")
            
            # Threads에 포스트 발행
            # instagrapi의 threads_upload 메소드 사용
            media = self.client.threads_upload(
                path=str(image_path),
                caption=caption
            )
            logger.info(f"✅ Threads 발행 완료 (ID: {media.pk})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Threads 업로드 오류: {str(e)}")
            return False
    
    def create_caption(self, stocks_data: dict) -> str:
        """Threads 캡션 생성"""
        try:
            current_date = datetime.now().strftime("%Y년 %m월 %d일")
            caption = f"📈 {current_date} 주식 브리핑\n\n"
            
            for screener_type, stocks in stocks_data.items():
                if not stocks:
                    continue
                
                if screener_type == "most_actives":
                    caption += "🔥 거래량 많은 종목\n"
                elif screener_type == "day_gainers":
                    caption += "📈 오늘의 상승 종목\n"
                elif screener_type == "day_losers":
                    caption += "📉 오늘의 하락 종목\n"
                else:
                    caption += f"{screener_type}\n"
                
                for i, stock in enumerate(stocks[:3], 1):
                    ticker = stock.get('symbol', 'N/A')
                    price = stock.get('price', 'N/A')
                    change = stock.get('change_percent', '0')
                    caption += f"{i}. {ticker} ${price} {change:+.2f}%\n"
                
                caption += "\n"
            
            caption += "\n#주식 #투자 #트렌드주 #화제종목 #주식시장 #주식정보"
            logger.info("✓ 캡션 생성 완료")
            return caption
            
        except Exception as e:
            logger.error(f"❌ 캡션 생성 오류: {e}")
            return "📈 주식 브리핑\n\n#주식 #투자 #트렌드주"
    
    def run(self) -> bool:
        """Threads 발행 실행"""
        try:
            if not self.login():
                logger.error("❌ Threads 로그인 실패")
                return False
            
            image_path = self.get_latest_image()
            stock_data = self.get_latest_stock_data()
            
            if not image_path or not stock_data:
                logger.warning("⚠️  필요한 데이터가 부족합니다.")
                return False
            
            caption = self.create_caption(stock_data)
            success = self.post_image(image_path, caption)
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Threads 서비스 오류: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def logout(self):
        """Threads 로그아웃"""
        try:
            if self.client:
                self.client.logout()
                logger.info("✓ Threads 로그아웃 완료")
        except Exception as e:
            logger.error(f"❌ 로그아웃 실패: {e}")


def main():
    """메인 실행 함수"""
    logger.info("=" * 60)
    logger.info("🚀 Threads 자동 발행 서비스 시작")
    logger.info("=" * 60)
    
    service = ThreadsService()
    
    if service.run():
        logger.info("=" * 60)
        logger.info("✅ Threads 발행 완료")
        logger.info("=" * 60)
        sys.exit(0)
    else:
        logger.error("=" * 60)
        logger.error("❌ Threads 발행 실패")
        logger.error("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
