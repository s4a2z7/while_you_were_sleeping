"""
yahooquery Screener dict 구조 확인
"""

from yahooquery import Screener
import json

screener = Screener()

print("most_actives 스크리너 결과 구조:")
print("="*60)

result = screener.get_screeners("most_actives")

print(f"타입: {type(result)}")
print(f"키: {result.keys() if hasattr(result, 'keys') else 'N/A'}")

if hasattr(result, 'keys'):
    for key in result.keys():
        print(f"\n  - {key}: {type(result[key])}")
        if key == 'quotes' and isinstance(result[key], list):
            print(f"    길이: {len(result[key])}")
            if len(result[key]) > 0:
                first_quote = result[key][0]
                print(f"    첫 번째 항목의 키: {list(first_quote.keys())[:10]}")  # 첫 10개만
                print(f"    첫 번째 종목:")
                print(f"      symbol: {first_quote.get('symbol')}")
                print(f"      longName: {first_quote.get('longName')}")
                print(f"      regularMarketPrice: {first_quote.get('regularMarketPrice')}")
