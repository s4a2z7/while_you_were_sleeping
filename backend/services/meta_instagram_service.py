"""
Meta Graph API를 사용한 Instagram 포스팅 서비스
공식 API를 사용하여 안정적인 포스팅
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
import json
import os
from dotenv import load_dotenv
import requests

# .env 파일 로드
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MetaInstagramService:
    """Meta Graph API를 사용한 Instagram 포스팅 서비스"""
    
    def __init__(self):
        """Meta Instagram 서비스 초기화"""
        self.access_token = os.getenv("META_ACCESS_TOKEN")
        self.business_account_id = os.getenv("META_INSTAGRAM_BUSINESS_ACCOUNT_ID")
        self.api_version = "v18.0"
        self.base_url = f"https://graph.instagram.com/{self.api_version}"
        
        self.data_dir = Path(__file__).parent.parent / "output" / "data"
        self.image_dir = Path(__file__).parent.parent / "output" / "images"
        
        if not self.access_token or not self.business_account_id:
            logger.warning("⚠️  Meta API 설정이 불완전합니다.")
            logger.warning(f"    META_ACCESS_TOKEN: {'✓' if self.access_token else '✗'}")
            logger.warning(f"    META_INSTAGRAM_BUSINESS_ACCOUNT_ID: {'✓' if self.business_account_id else '✗'}")
            return
        
        logger.info("✓ Meta Instagram 클라이언트 초기화 완료")
    
    def get_latest_image(self):
        """최신 브리핑 이미지 찾기"""
        if not self.image_dir.exists():
            logger.error("❌ 이미지 폴더가 없습니다.")
            return None
        
        images = list(self.image_dir.glob("briefing_card_*.png"))
        if not images:
            logger.error("❌ 브리핑 이미지가 없습니다.")
            return None
        
        latest = sorted(images, reverse=True)[0]
        logger.info(f"✓ 최신 이미지: {latest.name}")
        return latest
    
    def get_latest_stock_data(self):
        """최신 스크리너 데이터 로드"""
        if not self.data_dir.exists():
            logger.error("❌ 데이터 폴더가 없습니다.")
            return None
        
        data_files = list(self.data_dir.glob("screener_results_*.json"))
        if not data_files:
            logger.error("❌ 스크리너 데이터가 없습니다.")
            return None
        
        latest = sorted(data_files, reverse=True)[0]
        try:
            with open(latest, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"✓ 스크리너 데이터 로드: {latest.name}")
            return data
        except Exception as e:
            logger.error(f"❌ 데이터 로드 실패: {e}")
            return None
    
    def create_caption(self, stock_data):
        """Instagram 포스트 캡션 생성"""
        caption = "📈 와일유어슬립 주식 브리핑\n\n"
        
        if stock_data:
            # 거래량 많은 종목
            if "most_actives" in stock_data and stock_data["most_actives"]:
                caption += "🔥 거래량 많은 종목\n"
                for i, stock in enumerate(stock_data["most_actives"][:3], 1):
                    symbol = stock.get("symbol", "N/A")
                    price = stock.get("price", "N/A")
                    change = stock.get("change", "N/A")
                    caption += f"{i}. {symbol} ${price} {change}%\n"
                caption += "\n"
            
            # 상승 종목
            if "day_gainers" in stock_data and stock_data["day_gainers"]:
                caption += "📈 오늘의 상승 종목\n"
                for i, stock in enumerate(stock_data["day_gainers"][:3], 1):
                    symbol = stock.get("symbol", "N/A")
                    price = stock.get("price", "N/A")
                    change = stock.get("change", "N/A")
                    caption += f"{i}. {symbol} ${price} {change}%\n"
                caption += "\n"
            
            # 하락 종목
            if "day_losers" in stock_data and stock_data["day_losers"]:
                caption += "📉 오늘의 하락 종목\n"
                for i, stock in enumerate(stock_data["day_losers"][:3], 1):
                    symbol = stock.get("symbol", "N/A")
                    price = stock.get("price", "N/A")
                    change = stock.get("change", "N/A")
                    caption += f"{i}. {symbol} ${price} {change}%\n"
        
        caption += "\n#주식 #투자 #트렌드주 #화제종목 #주식시장"
        return caption
    
    def upload_image_to_instagram(self, image_path):
        """이미지를 Instagram에 업로드"""
        try:
            logger.info("📸 이미지 업로드 중...")
            
            url = f"{self.base_url}/{self.business_account_id}/media"
            
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                data = {
                    'media_type': 'IMAGE',
                    'access_token': self.access_token
                }
                
                response = requests.post(url, files=files, data=data)
            
            if response.status_code != 200:
                logger.error(f"❌ 이미지 업로드 실패: {response.status_code}")
                logger.error(f"   응답: {response.text}")
                return None
            
            media_id = response.json().get('id')
            logger.info(f"✓ 이미지 업로드 완료: {media_id}")
            return media_id
        
        except Exception as e:
            logger.error(f"❌ 이미지 업로드 오류: {e}")
            return None
    
    def publish_media(self, media_id, caption):
        """미디어를 Instagram에 발행"""
        try:
            logger.info("📱 Instagram 포스팅 중...")
            
            url = f"{self.base_url}/{self.business_account_id}/media_publish"
            
            data = {
                'creation_id': media_id,
                'caption': caption,
                'access_token': self.access_token
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code != 200:
                logger.error(f"❌ 포스팅 실패: {response.status_code}")
                logger.error(f"   응답: {response.text}")
                return False
            
            post_id = response.json().get('id')
            logger.info(f"✅ Instagram 포스팅 성공: {post_id}")
            return True
        
        except Exception as e:
            logger.error(f"❌ 포스팅 오류: {e}")
            return False
    
    def run(self):
        """Instagram 포스팅 실행"""
        logger.info("=" * 70)
        logger.info("🚀 Meta Instagram 자동 포스팅 서비스 시작")
        logger.info("=" * 70)
        
        # 설정 확인
        if not self.access_token or not self.business_account_id:
            logger.error("❌ Meta API 설정이 불완전합니다.")
            logger.error("❌ Instagram 포스팅 실패")
            logger.error("=" * 70)
            return False
        
        # 이미지 확인
        image = self.get_latest_image()
        if not image:
            logger.error("❌ Instagram 포스팅 실패")
            logger.error("=" * 70)
            return False
        
        # 데이터 확인
        stock_data = self.get_latest_stock_data()
        if not stock_data:
            logger.error("❌ Instagram 포스팅 실패")
            logger.error("=" * 70)
            return False
        
        # 캡션 생성
        caption = self.create_caption(stock_data)
        logger.info(f"✓ 캡션 생성 완료 ({len(caption)}자)")
        
        # 이미지 업로드
        media_id = self.upload_image_to_instagram(image)
        if not media_id:
            logger.error("❌ Instagram 포스팅 실패")
            logger.error("=" * 70)
            return False
        
        # 포스팅 발행
        if self.publish_media(media_id, caption):
            logger.info("=" * 70)
            logger.info("✅ Meta Instagram 포스팅 완료")
            logger.info("=" * 70)
            return True
        else:
            logger.error("=" * 70)
            logger.error("❌ Instagram 포스팅 실패")
            logger.error("=" * 70)
            return False


if __name__ == "__main__":
    service = MetaInstagramService()
    success = service.run()
    sys.exit(0 if success else 1)
