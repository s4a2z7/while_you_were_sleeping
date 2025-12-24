# 이미지 생성 명령어

## 설명
당신이 잠든 사이 브리핑 카드 이미지 및 관련 리소스를 생성합니다.

## 사용 가능한 생성기

### 1. 브리핑 카드 이미지 (PNG)
화제 종목 정보를 포함한 1200x630px 소셜 미디어 카드 이미지 생성

```bash
python generate_briefing_card.py
```

**저장 위치**: `output/images/briefing_card_20251205.png`

**포함 내용**:
- 제목: "당신이 잠든 사이" + 날짜
- 화제 종목 정보 (티커, 이름, 가격, 변동률)
- 선정 기준
- 배경: 다크 모드 (네이비 + 보라색 그라디언트)
- 강조색: 초록색 (#10B981) - 상승, 주황색 (#F59E0B) - 강조

### 2. 브리핑 리포트 (Word)
전문적인 워드 문서 포맷의 브리핑 보고서 생성

```bash
python generate_briefing_report.py
```

**저장 위치**: `output/reports/briefing_2025-12-05.docx`

**포함 내용**:
- 제목 및 날짜
- 오늘의 화제 종목 (정보 표)
- 왜 화제인가? (글머리 기호)
- 관련 뉴스 TOP 3
- 전문적 포맷팅 (초록색 강조, 표, 글머리)

### 3. 화제 종목 데이터 (Excel)
화제 종목 TOP 5 데이터를 엑셀 형식으로 생성

```bash
python generate_trending_excel.py
```

**저장 위치**: `output/data/trending_2025-12-05.xlsx`

**포함 내용**:
- 순위, 티커, 종목명, 주가, 등락률
- 색상 포맷팅: 상승 초록색, 하락 빨간색
- 헤더: 진한 파란색 배경
- 자동 정렬 및 테두리

## 설치 요구사항

```bash
# 이미지 생성용
pip install Pillow

# Word 문서용
pip install python-docx

# Excel 파일용
pip install openpyxl
```

## 출력 디렉토리 구조

```
output/
├── images/
│   └── briefing_card_20251205.png
├── reports/
│   └── briefing_2025-12-05.docx
└── data/
    └── trending_2025-12-05.xlsx
```

## 커스터마이징 옵션

### 브리핑 카드 이미지
- `generate_briefing_card.py` 수정
- `WIDTH`, `HEIGHT`: 이미지 크기 조정
- `BG_DARK`, `ACCENT_GREEN`: 색상 변경
- 날짜, 종목명, 뉴스 내용 수정

### 브리핑 리포트
- `generate_briefing_report.py` 수정
- `news_items` 리스트: 뉴스 항목 변경
- `reasons` 리스트: 화제 이유 변경
- 폰트, 색상, 레이아웃 커스터마이징

### 트렌딩 데이터
- `generate_trending_excel.py` 수정
- `data` 리스트: 종목 데이터 추가/변경
- 색상, 폰트, 열 너비 조정

## 자동화 예시

모든 생성기를 한 번에 실행:
```bash
python generate_briefing_card.py && python generate_briefing_report.py && python generate_trending_excel.py
```

## 품질 검사

생성된 파일들:
- PNG: 1200x630px, 약 16KB
- DOCX: 36KB, 5개 섹션
- XLSX: 6개 행, 5개 열, 컬러 포맷팅

## 참고사항
- 모든 이미지/문서는 하드코딩된 데이터로 생성됩니다
- 동적 데이터 연결을 원하면 API와 통합 필요
- 다국어 지원: 현재 한국어만 지원
