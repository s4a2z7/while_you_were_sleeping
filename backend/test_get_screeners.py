"""
yahooquery Screener get_screeners 메서드 테스트
"""

from yahooquery import Screener

screener = Screener()

# available_screeners 확인
print("사용 가능한 스크리너:")
print("="*60)
print(screener.available_screeners)

# get_screeners 메서드 사용
print("\n" + "="*60)
print("get_screeners() 호출 결과:")
print("="*60)

screeners_list = screener.available_screeners
print(f"\n이용 가능한 스크리너: {screeners_list}")

# 각 스크리너에 대해 시도
for screener_name in screeners_list:
    print(f"\n스크리너: {screener_name}")
    try:
        result = screener.get_screeners(screener_name)
        print(f"  타입: {type(result)}")
        if hasattr(result, 'shape'):
            print(f"  shape: {result.shape}")
        if hasattr(result, 'head'):
            print(f"  첫 행:\n{result.head(1)}")
    except Exception as e:
        print(f"  실패: {e}")
