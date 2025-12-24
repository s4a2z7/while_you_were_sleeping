"""
yahooquery Screener dict 구조 상세 확인
"""

from yahooquery import Screener
import json

screener = Screener()
result = screener.get_screeners("most_actives")

print("result 키:", result.keys())
inner_dict = result['most_actives']
print("inner_dict 키:", inner_dict.keys())
print()

for key in inner_dict.keys():
    value = inner_dict[key]
    print(f"{key}: {type(value)}")
    if key == 'quotes' and isinstance(value, list) and len(value) > 0:
        first = value[0]
        print(f"  첫 번째 항목 타입: {type(first)}")
        if isinstance(first, dict):
            print(f"  첫 번째 항목의 키:")
            for k in list(first.keys())[:15]:
                print(f"    - {k}")
            print(f"\n  첫 번째 종목 정보:")
            print(f"    symbol: {first.get('symbol')}")
            print(f"    longName: {first.get('longName')}")
            print(f"    regularMarketPrice: {first.get('regularMarketPrice')}")
