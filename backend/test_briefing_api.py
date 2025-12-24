"""
브리핑 생성 API 테스트
"""

import requests
import json
from pprint import pprint

# API 엔드포인트
BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/api/briefing/generate"

# 테스트 요청 데이터
test_cases = [
    {"ticker": "NVDA", "type": "most_actives"},
    {"ticker": "TSLA", "type": "day_gainers"},
    {"ticker": "AAPL", "type": "day_losers"},
]

print("=" * 80)
print("브리핑 생성 API 테스트")
print("=" * 80)

for i, test_data in enumerate(test_cases, 1):
    print(f"\n[테스트 {i}] {test_data['ticker']} - {test_data['type']}")
    print("-" * 80)
    
    try:
        # POST 요청
        response = requests.post(
            ENDPOINT,
            json=test_data,
            timeout=10
        )
        
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"결과:")
            print(f"  - 상태: {data.get('status')}")
            print(f"  - 티커: {data.get('ticker')}")
            print(f"  - 메시지: {data.get('message')}")
            
            # 콘텐츠는 처음 500자만 출력
            content = data.get('content', '')
            print(f"  - 콘텐츠 (처음 500자):")
            print("    " + "\n    ".join(content[:500].split("\n")))
            print("\n    ...")
        else:
            print(f"에러: {response.text}")
    
    except Exception as e:
        print(f"요청 실패: {str(e)}")

print("\n" + "=" * 80)
print("테스트 완료")
print("=" * 80)
