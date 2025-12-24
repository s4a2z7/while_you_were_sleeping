"""
yahooquery Screener API 탐색
"""

from yahooquery import Screener

# Screener 객체 생성
screener = Screener()

# 사용 가능한 메서드 출력
print("Screener 객체의 모든 속성 및 메서드:")
print("="*60)
attributes = [attr for attr in dir(screener) if not attr.startswith('_')]
for attr in attributes:
    print(f"  - {attr}")

print("\n" + "="*60)
print("직접 메서드 시도:")
print("="*60)

# 가능한 방식들 시도
try:
    print("\n1. screener.most_actives() 시도...")
    result = screener.most_actives()
    print(f"   성공! 결과 타입: {type(result)}")
    if hasattr(result, 'shape'):
        print(f"   shape: {result.shape}")
    if hasattr(result, 'head'):
        print(f"   첫 행:\n{result.head(1)}")
except Exception as e:
    print(f"   실패: {e}")

try:
    print("\n2. screener.day_gainers() 시도...")
    result = screener.day_gainers()
    print(f"   성공! 결과 타입: {type(result)}")
except Exception as e:
    print(f"   실패: {e}")

try:
    print("\n3. screener['most_actives'] 시도...")
    result = screener['most_actives']
    print(f"   성공! 결과 타입: {type(result)}")
except Exception as e:
    print(f"   실패: {e}")

try:
    print("\n4. screener.get('most_actives') 시도...")
    result = screener.get('most_actives')
    print(f"   성공! 결과 타입: {type(result)}")
except Exception as e:
    print(f"   실패: {e}")

# Screener의 __call__ 메서드 확인
print("\n" + "="*60)
print("Screener 호출 가능성 확인:")
print("="*60)
print(f"callable(screener): {callable(screener)}")

try:
    print("\n5. screener('most_actives') 시도...")
    result = screener('most_actives')
    print(f"   성공! 결과 타입: {type(result)}")
    if hasattr(result, 'shape'):
        print(f"   shape: {result.shape}")
except Exception as e:
    print(f"   실패: {e}")
