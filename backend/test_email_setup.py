#!/usr/bin/env python3
"""
이메일 발송 테스트 스크립트
로컬에서 Gmail SMTP 연결 테스트
"""

import os
import sys
import smtplib
import socket
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"✓ .env 파일 로드: {env_file}")
else:
    print(f"⚠️  .env 파일 없음: {env_file}")

# 환경 변수 확인
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

print("\n" + "=" * 60)
print("📧 이메일 발송 테스트")
print("=" * 60)
print(f"SMTP_SERVER: {SMTP_SERVER}")
print(f"SMTP_PORT: {SMTP_PORT}")
print(f"SENDER_EMAIL: {SENDER_EMAIL if SENDER_EMAIL else '❌ 미설정'}")
print(f"SENDER_PASSWORD: {'✓ 설정됨' if SENDER_PASSWORD else '❌ 미설정'}")
print(f"RECIPIENT_EMAIL: {RECIPIENT_EMAIL if RECIPIENT_EMAIL else '❌ 미설정'}")
print("=" * 60)

# 필수 설정 확인
if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
    print("❌ 필수 설정 누락!")
    sys.exit(1)

# Step 1: DNS 테스트
print("\n[1/4] DNS 해석 테스트...")
try:
    ip = socket.gethostbyname(SMTP_SERVER)
    print(f"✓ {SMTP_SERVER} → {ip}")
except socket.gaierror as e:
    print(f"❌ DNS 해석 실패: {e}")
    sys.exit(1)

# Step 2: SMTP 연결 테스트
print("\n[2/4] SMTP 서버 연결 테스트...")
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
        print(f"✓ SMTP 서버 연결 성공")
        
        # Step 3: TLS 테스트
        print("\n[3/4] TLS 암호화 테스트...")
        server.starttls()
        print(f"✓ TLS 활성화 완료")
        
        # Step 4: 인증 테스트
        print("\n[4/4] Gmail 인증 테스트...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print(f"✓ 인증 성공")
        
        print("\n" + "=" * 60)
        print("✅ 모든 테스트 통과!")
        print("=" * 60)
        print(f"이제 GitHub에서 이메일을 수신할 준비가 되었습니다.")
        print(f"\nGitHub Secrets에서 다음 값들을 설정하세요:")
        print(f"  SMTP_SERVER = {SMTP_SERVER}")
        print(f"  SMTP_PORT = {SMTP_PORT}")
        print(f"  SENDER_EMAIL = {SENDER_EMAIL}")
        print(f"  SENDER_PASSWORD = [16자리 앱 비밀번호]")
        print(f"  RECIPIENT_EMAIL = {RECIPIENT_EMAIL}")
        
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ 인증 실패: {e}")
    print(f"\n확인사항:")
    print(f"1. Gmail 주소가 정확한가? ({SENDER_EMAIL})")
    print(f"2. 앱 비밀번호가 올바른가? (16자리)")
    print(f"3. 2단계 인증이 활성화되어 있는가?")
    print(f"4. 앱 비밀번호를 최근에 생성했는가?")
    sys.exit(1)
    
except smtplib.SMTPException as e:
    print(f"❌ SMTP 오류: {e}")
    sys.exit(1)
    
except socket.timeout:
    print(f"❌ 연결 타임아웃 (10초)")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
