# GitHub Actions 설정 가이드

## 📋 개요
자동으로 매일 아침 7시(한국시간)에 실행되는 주식 브리핑 자동화 워크플로우입니다.

---

## 🔧 워크플로우 파일
- **위치**: `.github/workflows/daily_briefing.yml`
- **실행 주기**: 매일 UTC 22:00 (한국시간 아침 7시)
- **수동 실행**: GitHub Actions 탭에서 "Run workflow" 버튼으로 언제든 수동 실행 가능

---

## 📍 실행 흐름

```
1. 의존성 설치 (pip install -r backend/requirements.txt)
   ↓
2. 화제 종목 조회 (python -m services.screener_service)
   └─ 3가지 스크리너 타입 조회 (most_actives, day_gainers, day_losers)
   └─ 결과 저장: output/data/screener_results_YYYYMMDD.json
   ↓
3. 브리핑 생성 (python -m services.briefing_generator)
   └─ 각 종목별 상세 브리핑 생성
   └─ 결과 저장: output/data/briefings_YYYYMMDD.json
   └─ 결과 저장: output/reports/briefing_YYYYMMDD.md
   ↓
4. 이메일 발송 (python -m services.email_service)
   └─ HTML 형식 이메일 발송
   └─ 마크다운 파일 첨부
```

---

## 🔐 환경 변수 설정 (GitHub Secrets)

### 1. GitHub Repository Settings에서 Secrets 추가

**경로**: Settings > Secrets and variables > Actions > New repository secret

### 2. 필수 환경 변수

#### SMTP 설정 (이메일 발송)
```bash
SMTP_SERVER       = smtp.gmail.com
SMTP_PORT         = 587
SENDER_EMAIL      = your-email@gmail.com
SENDER_PASSWORD   = your-app-password  # 구글의 경우 앱 비밀번호 사용
RECIPIENT_EMAIL   = recipient@example.com
```

#### API 키
```bash
EXA_API_KEY       = your-exa-api-key  # 선택사항 (뉴스 조회)
```

### 3. Gmail 앱 비밀번호 생성 방법

1. [Google Account](https://myaccount.google.com)에 접속
2. 보안(Security) 탭으로 이동
3. "2-Step Verification" 활성화
4. "App passwords" 생성
5. 생성된 16자리 비밀번호를 `SENDER_PASSWORD`로 사용

---

## 🚀 사용 방법

### 1. 워크플로우 활성화 확인
```bash
# 저장소에 .github/workflows/daily_briefing.yml이 있는지 확인
ls -la .github/workflows/
```

### 2. GitHub 웹 인터페이스에서 수동 실행

1. GitHub Repository로 이동
2. Actions 탭 클릭
3. "Daily Stock Briefing" 워크플로우 선택
4. "Run workflow" > "Run workflow" 버튼 클릭

### 3. 로컬에서 테스트

```bash
# 의존성 설치
pip install -r backend/requirements.txt

# 화제 종목 조회
cd backend
python -m services.screener_service

# 브리핑 생성
python -m services.briefing_generator

# 이메일 발송 (환경 변수 설정 필요)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="recipient@example.com"
python -m services.email_service
```

---

## 📊 출력 파일

### 스크리너 결과
```
backend/output/data/screener_results_20251224.json
```
```json
{
  "most_actives": {
    "status": "success",
    "screener_type": "most_actives",
    "top_stock": {
      "ticker": "TSLA",
      "name": "Tesla, Inc.",
      "price": 385.20,
      "change_percent": 8.7,
      ...
    }
  },
  ...
}
```

### 브리핑 데이터
```
backend/output/data/briefings_20251224.json
backend/output/reports/briefing_20251224.md
```

---

## 🔍 로그 확인

### GitHub Actions에서 로그 보기

1. GitHub Repository > Actions 탭
2. "Daily Stock Briefing" 워크플로우 선택
3. 실행 내역에서 작업을 클릭하면 상세 로그 확인 가능

### 각 단계별 로그
- `Set up Python 3.12` - Python 설정
- `Install dependencies` - 패키지 설치
- `Run Screener Service` - 화제 종목 조회
- `Generate Briefing` - 브리핑 생성
- `Send Email` - 이메일 발송
- `Notify Success/Failure` - 최종 결과

---

## ⚠️ 문제 해결

### 1. "No such file or directory" 오류
**원인**: 서비스 파일을 찾을 수 없음
```
ModuleNotFoundError: No module named 'services.screener_service'
```
**해결**: 
- `backend/services/screener_service.py` 파일 존재 확인
- 파일이 올바른 위치에 있는지 확인

### 2. SMTP 인증 실패
**원인**: 이메일 설정이 잘못됨
```
SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted')
```
**해결**:
- Gmail을 사용하는 경우 "앱 비밀번호" 생성 필요
- SENDER_PASSWORD에 일반 비밀번호가 아닌 앱 비밀번호 사용

### 3. "EXA_API_KEY 환경 변수 설정 없음" 경고
**원인**: Exa API 키가 설정되지 않음
```
WARNING: EXA_API_KEY 환경 변수가 설정되지 않았습니다.
```
**해결**: 선택사항이므로 무시 가능. 뉴스 기능을 사용하려면 설정

### 4. "브리핑 파일을 찾을 수 없습니다" 오류
**원인**: briefing_generator가 실행되지 않음
```
WARNING: 브리핑 파일을 찾을 수 없습니다.
```
**해결**:
- `Generate Briefing` 단계 로그 확인
- screener_service가 성공적으로 실행되었는지 확인

---

## 📈 모니터링

### 예상 실행 결과
```
2025-12-24 22:00 UTC (2025-12-25 07:00 KST)
├── ✅ Checkout code
├── ✅ Set up Python 3.12
├── ✅ Install dependencies
├── ✅ Run Screener Service
│   ├── ✅ most_actives: TSLA
│   ├── ✅ day_gainers: NVDA
│   └── ✅ day_losers: F
├── ✅ Generate Briefing
│   ├── ✅ TSLA 브리핑 생성
│   ├── ✅ NVDA 브리핑 생성
│   └── ✅ F 브리핑 생성
├── ✅ Send Email
│   └── ✅ recipient@example.com으로 발송
└── ✅ Notify Success
```

---

## 🔔 알림 설정

### 이메일 알림
- GitHub Actions > Notifications > Email 설정
- "On workflow failure" 체크로 실패 시에만 알림

### 선택사항: Slack/Discord 통지 추가

**Slack 예시**:
```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 📅 스케줄 변경 방법

### 현재 설정
```yaml
schedule:
  - cron: '0 22 * * *'  # UTC 22:00 = KST 07:00
```

### 다른 시간으로 변경 예시

```yaml
# 매일 오전 10시 (UTC 01:00)
- cron: '0 1 * * *'

# 평일 오전 7시 (UTC 22:00, Mon-Fri)
- cron: '0 22 * * 1-5'

# 매주 월요일 오전 7시
- cron: '0 22 * * 1'

# 매월 1일 오전 7시
- cron: '0 22 1 * *'
```

---

## 💾 데이터 보관

### 출력 파일 저장
- 로컬 저장: `backend/output/data/`, `backend/output/reports/`
- GitHub Actions 아티팩트로 저장 (선택사항):

```yaml
- name: Upload artifacts
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: briefing-reports-${{ matrix.os }}
    path: backend/output/
    retention-days: 30
```

---

## 🚨 보안 주의사항

1. **절대 비밀번호를 코드에 작성하면 안 됨**
   - 항상 GitHub Secrets 사용

2. **민감한 정보 보호**
   - 로그에 민감한 정보 출력 금지
   - 이메일 주소 마스킹 권장

3. **주기적 보안 감사**
   - Secrets 정기적 갱신
   - GitHub Security 탭에서 취약점 확인

---

## 📞 지원

문제 발생 시:
1. GitHub Actions 로그 확인
2. 환경 변수 설정 재확인
3. 로컬에서 각 서비스 테스트
4. Issue 등록

---

**Last Updated**: 2025-12-24
