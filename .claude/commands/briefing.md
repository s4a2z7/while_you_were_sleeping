# 브리핑 생성 명령어

## 설명
화제 종목 기반 브리핑 콘텐츠를 마크다운 형식으로 생성합니다.

## 사용법
```bash
python backend/test_briefing_api.py
```

## API 엔드포인트
- **POST** `/api/briefing/generate`
- **GET** `/api/briefing/generate?ticker=TSLA&type=most_actives`

## 요청 예시
```json
{
  "ticker": "TSLA",
  "type": "most_actives"
}
```

## 응답 포맷
```json
{
  "status": "success",
  "ticker": "TSLA",
  "content": "# TSLA - Tesla, Inc. 브리핑\n\n...",
  "message": "TSLA 브리핑이 생성되었습니다."
}
```

## 스크리너 타입
- `most_actives`: 가장 활발한 거래량 종목
- `day_gainers`: 오늘 상승 종목
- `day_losers`: 오늘 하락 종목

## 브리핑 내용 구성
1. **종목 정보 표**: 주가, 변동률, 거래량, 시가총액, 섹터, 산업, PER
2. **관련 뉴스**: 최대 5개의 관련 뉴스 기사
3. **분석 요약**: 가격 동향, 거래 활동, 기본 정보, 밸류에이션

## 관련 파일
- `backend/services/briefing_service.py` - 브리핑 생성 로직
- `backend/api/briefings.py` - API 엔드포인트
- `backend/services/stock_service.py` - 종목 정보 조회
- `backend/services/news_service.py` - 뉴스 조회

## 참고사항
- EXA_API_KEY가 설정되지 않으면 뉴스는 빈 배열로 반환됩니다
- 모든 시간은 UTC 기준입니다
- 마크다운 포맷으로 생성되므로 HTML/PDF로 변환 가능합니다
