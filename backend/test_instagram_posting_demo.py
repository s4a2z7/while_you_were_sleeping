#!/usr/bin/env python3
"""
테스트용 인스타그램 포스팅 데모 스크립트
(실제 인스타그램 계정에 포스트하지 않고 결과만 출력)
"""

import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image

# 설정
OUTPUT_DIR = Path(__file__).parent.parent / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
DATA_DIR = OUTPUT_DIR / "data"

def get_latest_image():
    """최신 브리핑 이미지 찾기"""
    images = list(IMAGES_DIR.glob("briefing_card_*.png"))
    if not images:
        return None
    return sorted(images)[-1]

def get_latest_stock_data():
    """최신 스크리너 데이터 로드"""
    data_files = list(DATA_DIR.glob("screener_results_*.json"))
    if not data_files:
        return None
    
    latest_file = sorted(data_files)[-1]
    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_caption(stock_data):
    """인스타그램 캡션 생성"""
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
    
    caption += "\n#주식 #투자 #트렌드주 #화제종목 #주식시장 #주식정보"
    return caption

def main():
    """메인 실행"""
    print("\n" + "="*70)
    print("📱 인스타그램 포스팅 테스트 데모")
    print("="*70 + "\n")
    
    # 1. 최신 이미지 확인
    print("[1/3] 브리핑 이미지 확인...")
    image_path = get_latest_image()
    if image_path:
        print(f"✅ 찾음: {image_path.name}")
        try:
            img = Image.open(image_path)
            print(f"   크기: {img.size[0]} x {img.size[1]} pixels")
        except Exception as e:
            print(f"   ⚠️  이미지 정보 로드 실패: {e}")
    else:
        print("❌ 이미지를 찾을 수 없습니다")
        return
    
    # 2. 스크리너 데이터 확인
    print("\n[2/3] 스크리너 데이터 확인...")
    stock_data = get_latest_stock_data()
    if stock_data:
        print(f"✅ 데이터 로드 완료")
        print(f"   거래량 많은 종목: {len(stock_data.get('most_actives', []))}개")
        print(f"   상승 종목: {len(stock_data.get('day_gainers', []))}개")
        print(f"   하락 종목: {len(stock_data.get('day_losers', []))}개")
    else:
        print("❌ 스크리너 데이터를 찾을 수 없습니다")
        return
    
    # 3. 캡션 생성 및 출력
    print("\n[3/3] 인스타그램 캡션 생성...")
    caption = create_caption(stock_data)
    print("✅ 캡션 생성 완료\n")
    
    print("="*70)
    print("📝 인스타그램 포스트 미리보기")
    print("="*70)
    print(caption)
    print("="*70)
    
    # 이미지 미리보기
    print(f"\n📸 포스트 이미지: {image_path.name}")
    print(f"   경로: {image_path}")
    
    # 최종 정보
    print("\n" + "="*70)
    print("✅ 테스트 완료!")
    print("="*70)
    print(f"""
📋 포스트 정보:
   - 이미지: {image_path.name}
   - 캡션 길이: {len(caption)} 글자
   - 해시태그: {caption.count('#')}개
   - 포스트 예정: 2025-12-25
   - 계정: @s4a2z7

💡 실제 포스팅하려면:
   python -m services.instagram_service

🔄 자동 포스팅:
   - GitHub Actions: 매일 07:00 AM (KST)
   - Windows Task Scheduler: 매일 07:00 AM (로컬)
""")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
