#!/usr/bin/env python3
"""
실제 이메일 발송 테스트
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_file = Path(__file__).parent / ".env"
load_dotenv(env_file)

# 서비스 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

from services.email_service import EmailService

# 테스트 브리핑 데이터
test_briefing = {
    "most_actives": [
        {"symbol": "NVDA", "name": "NVIDIA", "price": 140.50, "change_percent": 2.5},
        {"symbol": "AAPL", "name": "Apple", "price": 250.30, "change_percent": 1.2}
    ],
    "day_gainers": [
        {"symbol": "MSTR", "name": "Microstrategy", "price": 420.50, "change_percent": 15.3},
        {"symbol": "COIN", "name": "Coinbase", "price": 125.80, "change_percent": 8.7}
    ],
    "day_losers": [
        {"symbol": "TSM", "name": "TSMC", "price": 120.50, "change_percent": -3.2},
        {"symbol": "AMD", "name": "AMD", "price": 180.25, "change_percent": -2.1}
    ]
}

print("\n" + "=" * 60)
print("📧 실제 이메일 발송 테스트")
print("=" * 60)

# 이메일 서비스 초기화
email_service = EmailService()

# 이메일 발송
success = email_service.send_briefing_email(test_briefing)

if success:
    print("\n✅ 이메일이 성공적으로 발송되었습니다!")
    print(f"   수신자: {email_service.recipient_email}")
    print(f"   발신자: {email_service.sender_email}")
else:
    print("\n❌ 이메일 발송에 실패했습니다.")
    sys.exit(1)
