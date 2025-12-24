#!/usr/bin/env python3
"""
인스타그램 자동 게시 테스트 스크립트
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def test_instagram_posting():
    """인스타그램 자동 게시 테스트"""
    
    print("\n" + "="*60)
    print("📱 인스타그램 자동 게시 테스트")
    print("="*60 + "\n")
    
    # 1. 환경변수 확인
    print("✅ Step 1: 환경변수 확인")
    instagram_username = os.getenv("INSTAGRAM_USERNAME")
    instagram_password = os.getenv("INSTAGRAM_PASSWORD")
    
    if not instagram_username:
        print("❌ INSTAGRAM_USERNAME이 설정되지 않았습니다!")
        print("   backend/.env 파일에 다음을 추가하세요:")
        print("   INSTAGRAM_USERNAME=your_username")
        return False
    
    if not instagram_password:
        print("❌ INSTAGRAM_PASSWORD가 설정되지 않았습니다!")
        print("   backend/.env 파일에 다음을 추가하세요:")
        print("   INSTAGRAM_PASSWORD=your_app_password")
        return False
    
    print(f"   ✅ 사용자명: {instagram_username}")
    print(f"   ✅ 앱 비밀번호: {'*' * len(instagram_password)}")
    
    # 2. instagrapi 설치 확인
    print("\n✅ Step 2: instagrapi 설치 확인")
    try:
        import instagrapi
        print(f"   ✅ instagrapi 설치됨 (v{instagrapi.__version__})")
    except ImportError:
        print("❌ instagrapi가 설치되지 않았습니다!")
        print("\n   설치 방법:")
        print("   1. 별도 환경 사용:")
        print("      python -m venv insta_env")
        print("      insta_env\\Scripts\\Activate.ps1")
        print("      pip install -r requirements_instagram.txt")
        print()
        print("   2. 또는 현재 환경에 설치:")
        print("      pip install instagrapi==2.0.0 --force-reinstall --no-deps")
        return False
    
    # 3. Instagram 서비스 테스트
    print("\n✅ Step 3: 인스타그램 서비스 로드")
    try:
        from services.instagram_service import InstagramService
        print("   ✅ InstagramService 로드 성공")
    except ImportError as e:
        print(f"❌ InstagramService 로드 실패: {e}")
        return False
    
    # 4. 로그인 테스트
    print("\n✅ Step 4: 인스타그램 로그인 테스트")
    try:
        service = InstagramService()
        if not service.client:
            print("❌ 인스타그램 클라이언트 초기화 실패")
            print("   instagrapi가 올바르게 설치되었는지 확인하세요")
            return False
        
        if service.login():
            print("   ✅ 로그인 성공!")
        else:
            print("❌ 로그인 실패")
            print("   • 사용자명 확인: INSTAGRAM_USERNAME")
            print("   • 앱 비밀번호 확인: INSTAGRAM_PASSWORD")
            print("   • 2단계 인증 설정 확인")
            print("   • 계정이 잠겨있지 않은지 확인")
            return False
    except Exception as e:
        print(f"❌ 로그인 중 오류: {e}")
        return False
    
    # 5. 최신 이미지 확인
    print("\n✅ Step 5: 브리핑 이미지 확인")
    latest_image = service.get_latest_image()
    if latest_image:
        print(f"   ✅ 이미지 찾음: {latest_image.name}")
    else:
        print("⚠️  이미지를 찾을 수 없습니다")
        print("   먼저 브리핑을 생성해주세요:")
        print("   python -m services.briefing_generator")
        return False
    
    # 6. 주식 데이터 확인
    print("\n✅ Step 6: 주식 데이터 확인")
    stock_data = service.get_latest_stock_data()
    if stock_data:
        print(f"   ✅ 데이터 로드 성공 ({len(stock_data)} 카테고리)")
        for category, stocks in stock_data.items():
            if stocks:
                print(f"      • {category}: {len(stocks)}개 종목")
    else:
        print("⚠️  주식 데이터를 찾을 수 없습니다")
        print("   먼저 스크리너를 실행해주세요:")
        print("   python -m services.screener_service")
        return False
    
    # 7. 캡션 생성 확인
    print("\n✅ Step 7: 캡션 생성")
    caption = service.create_caption(stock_data)
    print(f"   ✅ 캡션 생성 성공 ({len(caption)}자)")
    print("\n" + "-"*60)
    print("📝 생성된 캡션:")
    print("-"*60)
    print(caption[:200] + "...")
    print("-"*60)
    
    # 8. 인스타그램 게시 여부 확인
    print("\n✅ Step 8: 게시 준비 완료")
    print("   다음 명령으로 실제 게시할 수 있습니다:")
    print("   python -m services.instagram_service")
    print()
    print("   또는 일일 자동 게시 설정:")
    print("   • Task Scheduler 설정 (이미 run_daily_briefing.py에 포함)")
    print("   • 매일 07:00 AM 자동 실행")
    
    return True


if __name__ == "__main__":
    try:
        success = test_instagram_posting()
        print("\n" + "="*60)
        if success:
            print("✅ 모든 테스트 성공! 인스타그램 준비 완료")
            print("="*60 + "\n")
            sys.exit(0)
        else:
            print("❌ 테스트 실패. 위의 단계를 확인하세요")
            print("="*60 + "\n")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
