"""
yahooquery Ticker API 탐색
"""

from yahooquery import Ticker

ticker_obj = Ticker("NVDA")

print("Ticker 객체의 모든 속성:")
print("="*60)
attributes = [attr for attr in dir(ticker_obj) if not attr.startswith('_')]
for attr in attributes[:30]:  # 처음 30개만
    print(f"  - {attr}")

print("\n" + "="*60)
print("각 속성 시도:")
print("="*60)

# 각 속성 시도
for attr in ['quote', 'income_statement', 'balance_sheet', 'cash_flow', 'summary_detail', 'asset_profile']:
    try:
        result = getattr(ticker_obj, attr, None)
        print(f"\n{attr}:")
        if result is not None:
            print(f"  타입: {type(result)}")
            if isinstance(result, dict):
                print(f"  키: {list(result.keys())[:10]}")
                # 첫 번째 키의 값 확인
                first_key = list(result.keys())[0]
                print(f"  {first_key}: {result[first_key]}")
        else:
            print(f"  None")
    except Exception as e:
        print(f"  오류: {e}")
