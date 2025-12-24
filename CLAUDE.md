# While You Were Sleeping - Claude Code 개발 프로세스 가이드

## 📋 프로젝트 개요

### 프로젝트명
**While You Were Sleeping** - 미국주식 데일리 브리핑 서비스

### 프로젝트 설명
사용자가 잠들어 있는 동안 발생한 미국 주식시장의 주요 뉴스와 종목 정보를 매일 아침 브리핑으로 제공하는 서비스

### 핵심 기능
- 일일 주식 시장 브리핑
- 종목별 상세 정보 조회
- AI 기반 뉴스 요약
- 실시간 주가 데이터

## 🛠️ 기술 스택

| 구성 | 기술 |
|------|------|
| **Frontend** | Next.js (React 18+, TypeScript) - 1주차 프로토타입 |
| **Backend** | FastAPI, Python 3.12+ |
| **데이터 수집** | yahooquery (Screener, 종목 정보) |
| **뉴스 검색** | Exa API |
| **AI** | Gemini API (뉴스 요약 및 분석) |
| **데이터베이스** | PostgreSQL (예정) |

## 📁 폴더 구조

```
while-you-were-sleeping-dashboard/
├── /app                 # Next.js 프론트엔드
│   ├── layout.tsx
│   ├── page.tsx
│   └── briefings/
├── /backend             # FastAPI 백엔드
│   ├── main.py
│   ├── api/
│   ├── services/
│   └── models/
├── /services            # 공유 비즈니스 로직
│   ├── data_collection/
│   ├── ai_analysis/
│   └── news_fetch/
├── /components          # React 컴포넌트
├── /lib                 # 유틸리티, 타입 정의
├── /public              # 정적 파일
├── /개발일지            # 개발 로그
├── CLAUDE.md            # 이 파일
└── package.json
```

## 📝 코딩 컨벤션

### 명명 규칙
| 대상 | 규칙 | 예시 |
|------|------|------|
| 함수명 | snake_case | `get_stock_data()`, `fetch_news()` |
| 클래스명 | PascalCase | `StockBriefing`, `NewsAnalyzer` |
| 상수명 | UPPER_SNAKE_CASE | `MAX_RETRIES`, `API_TIMEOUT` |
| 변수명 | snake_case | `current_price`, `market_data` |
| 파일명 | snake_case | `stock_service.py`, `briefing_model.ts` |

### 주석 및 문서화
- **주석 언어**: 한글 (명확한 의사소통을 위해)
- **함수 주석**: JSDoc/docstring 형식
- **복잡한 로직**: 단계별 설명 주석 추가

### TypeScript/Python 코드 스타일
```typescript
// TypeScript 예시
// 사용자 브리핑 데이터 조회
async function getBriefingData(userId: string): Promise<Briefing> {
  // ...
}
```

```python
# Python 예시
# 주식 데이터 수집 및 분석
def collect_stock_data(tickers: List[str]) -> Dict[str, StockInfo]:
    # ...
```

---

## 개발일지 작성 규칙

### 파일 네이밍 규칙
- 형식: `YYYY-MM-DD_HH-mm_주제.md`
- 예: `2025-12-17_19-30_API_구현.md`
- 모든 개발일지는 `개발일지/` 폴더에 저장

### 개발일지 작성 템플릿

```markdown
# [주제]

## 작성 정보
- **작성 시간**: YYYY-MM-DD HH:mm
- **담당자**: [개발자명]
- **관련 파일**: [수정된 파일들]

## 해결하고자 한 문제
- [문제 1]
- [문제 2]

## 진행 사항

### ✅ 해결된 것
- [완료된 작업 1]
- [완료된 작업 2]

### ❌ 해결되지 않은 것
- [미해결 문제 1] (사유: [이유])
- [미해결 문제 2] (사유: [이유])

## 향후 개발을 위한 컨텍스트

### 현재 상태
- [현재 구현 상태 설명]

### 다음 단계
- [ ] [다음 할 작업 1]
- [ ] [다음 할 작업 2]

### 주의사항
- [주의할 점 1]
- [주의할 점 2]

### 참고 자료
- [관련 문서 링크]
- [참고 코드]

---
```

## 백엔드 개발 프로세스

### 1. API 함수/클래스 구현 단계

#### 단계별 체크리스트
1. **설계 단계**
   - [ ] 함수/클래스의 목적 명확히 정의
   - [ ] 입력/출력 타입 정의
   - [ ] 에러 케이스 정의

2. **구현 단계**
   - [ ] 코드 구현
   - [ ] JSDoc/TSDoc 주석 추가
   - [ ] 타입 안정성 검증

3. **테스트 단계** (필수)
   - [ ] 단위 테스트 작성
   - [ ] 정상 케이스 테스트
   - [ ] 에러 케이스 테스트
   - [ ] 엣지 케이스 테스트
   - [ ] 모든 테스트 통과 확인

4. **검증 단계**
   - [ ] 코드 리뷰
   - [ ] 성능 체크
   - [ ] 보안 검토

5. **다음 단계 진행**
   - 위의 모든 단계 완료 후에만 다음 작업 시작

### 2. 테스트 작성 표준

```typescript
// 테스트 파일 위치: __tests__/[기능명].test.ts

describe('API 함수명', () => {
  describe('정상 케이스', () => {
    test('should return expected result', () => {
      // 테스트 코드
    });
  });

  describe('에러 케이스', () => {
    test('should throw error when input is invalid', () => {
      // 테스트 코드
    });
  });

  describe('엣지 케이스', () => {
    test('should handle edge case correctly', () => {
      // 테스트 코드
    });
  });
});
```

### 3. 커밋 메시지 규칙

```
feat: [기능명] - [설명]
- [변경사항 1]
- [변경사항 2]

테스트: [테스트 결과 요약]
```

## 개발 중 유의사항

- **한 번에 하나의 기능만 작업**
- **테스트 없이 다음 단계로 진행 금지**
- **모든 변경사항은 개발일지에 기록**
- **의존성 추가 시 package.json에 기록**
- **타입 안정성 유지 (TypeScript strict mode)**

## 프로젝트 구조

```
while-you-were-sleeping-dashboard/
├── app/                  # Next.js 앱 라우터
├── components/           # React 컴포넌트
├── lib/                  # 유틸리티, 타입, API
├── public/               # 정적 파일
├── __tests__/            # 테스트 파일
├── 개발일지/             # 개발 로그
├── CLAUDE.md            # 이 파일
└── package.json         # 의존성
```

---
**마지막 업데이트**: 2025-12-17
