"""
yahooquery Ticker 테스트
"""
from yahooquery import Ticker
import json

ticker = Ticker("NVDA")

print("=== asset_profile ===")
print(json.dumps(dict(ticker.asset_profile), indent=2, default=str)[:500])

print("\n=== summary_detail ===")
summary = ticker.summary_detail
print(type(summary))
if isinstance(summary, dict):
    print(json.dumps({k: v for k, v in list(summary.items())[:5]}, indent=2, default=str))

print("\n=== key info ===")
try:
    summary_dict = dict(summary) if hasattr(summary, 'items') else summary
    if "NVDA" in summary_dict:
        nvda = summary_dict["NVDA"]
        print(f"Price: {nvda.get('regularMarketPrice')}")
        print(f"Volume: {nvda.get('regularMarketVolume')}")
except Exception as e:
    print(f"Error: {e}")
