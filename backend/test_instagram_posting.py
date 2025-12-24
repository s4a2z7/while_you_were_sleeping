#!/usr/bin/env python3
"""
인스타그램 게시 테스트
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

print("\n" + "="*60)
print("🧪 인스타그램 게시 테스트")
print("="*60 + "\n")

# 1. 환경변수 확인
print("✅ Step 1: 환경변수 확인")
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

if username and password:
    print(f"   ✅ 사용자명: {username}")
    print(f"   ✅ 비밀번호: {'*' * len(password)}")
else:
    print("   ❌ Instagram 설정이 필요합니다")
    sys.exit(1)

# 2. 이미지 확인
print("\n✅ Step 2: 브리핑 이미지 확인")
output_dir = Path("../output/images")
images = list(output_dir.glob("briefing_card_*.png"))

if images:
    latest_image = sorted(images)[-1]
    print(f"   ✅ 이미지 찾음: {latest_image.name}")
    print(f"   📦 크기: {latest_image.stat().st_size / 1024:.1f} KB")
else:
    print("   ❌ 이미지를 찾을 수 없습니다")
    print("   먼저 python -m services.briefing_generator 실행하세요")
    sys.exit(1)

# 3. 주식 데이터 확인
print("\n✅ Step 3: 주식 데이터 확인")
import json
data_dir = Path("../output/data")
data_files = list(data_dir.glob("screener_results_*.json"))

if data_files:
    latest_data = sorted(data_files)[-1]
    with open(latest_data, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"   ✅ 데이터 찾음: {latest_data.name}")
    print(f"   📊 카테고리: {len(data)}개")
    for category, stocks in data.items():
        if stocks:
            print(f"      • {category}: {len(stocks)}개 종목")
else:
    print("   ❌ 데이터를 찾을 수 없습니다")
    sys.exit(1)

# 4. Instagram 서비스 로드
print("\n✅ Step 4: Instagram 서비스 로드")
try:
    from services.instagram_service import InstagramService
    print("   ✅ 서비스 로드 성공")
except ImportError as e:
    print(f"   ❌ 로드 실패: {e}")
    sys.exit(1)

# 5. 캡션 미리보기
print("\n✅ Step 5: 캡션 미리보기")
service = InstagramService()
caption = service.create_caption(data)
print(f"   📝 캡션 길이: {len(caption)}자")
print("\n" + "-"*60)
print(caption[:300] + "...")
print("-"*60)

print("\n" + "="*60)
print("✅ 모든 테스트 완료!")
print("="*60)
print("\n📱 인스타그램 게시 준비 완료!")
print("\n다음 명령으로 Docker를 통해 게시하세요:")
print("   .\run_instagram_docker.ps1")
print("\n또는 Docker Desktop 설치 후:")
print("   .\deploy_instagram.ps1")
print("\n" + "="*60 + "\n")
