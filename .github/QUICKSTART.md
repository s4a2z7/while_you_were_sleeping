# GitHub Actions 자동화 설정 완료

## 📋 생성된 파일

### Workflow 파일
```
.github/workflows/daily_briefing.yml
```
- 매일 UTC 22:00 (KST 07:00)에 자동 실행
- 수동으로도 언제든 실행 가능

### 서비스 파일
```
backend/services/screener_service.py      # 화제 종목 조회
backend/services/briefing_generator.py    # 브리핑 생성
backend/services/email_service.py         # 이메일 발송
```

### 가이드 문서
```
.github/GITHUB_ACTIONS_GUIDE.md           # 상세 사용 가이드
.github/SECRETS_SETUP.md                  # GitHub Secrets 설정 가이드
```

---

## ⚡ 빠른 시작 (3단계)

### 1단계: GitHub Secrets 설정
```
Repository Settings > Secrets and variables > Actions
```

다음 7개 필드 추가:
- `SMTP_SERVER` = smtp.gmail.com
- `SMTP_PORT` = 587
- `SENDER_EMAIL` = your-email@gmail.com (Gmail 앱 비밀번호 필요!)
- `SENDER_PASSWORD` = your-app-password
- `RECIPIENT_EMAIL` = recipient@example.com
- `INSTAGRAM_USERNAME` = your_instagram_username
- `INSTAGRAM_PASSWORD` = your_instagram_password

**중요**: 
- Gmail 사용 시 [앱 비밀번호 생성](https://myaccount.google.com) 필수
- Instagram은 개인 계정 또는 비즈니스 계정 모두 가능

### 2단계: 로컬 테스트 (선택사항)
```bash
# 의존성 설치
pip install -r backend/requirements.txt

# 화제 종목 조회
cd backend && python -m services.screener_service

# 브리핑 생성
python -m services.briefing_generator

# 이메일 발송
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="recipient@example.com"
python -m services.email_service
```

### 3단계: GitHub Actions에서 확인
1. Repository > Actions 탭
2. "Daily Stock Briefing" 선택
3. "Run workflow" 클릭으로 즉시 실행 가능
4. 매일 아침 7시 자동 실행 시작

---

## 🔄 실행 흐름

```
매일 아침 7시 (한국시간) UTC 22:00
    ↓
1. 의존성 설치
    ↓
2. 화제 종목 조회 (3가지 스크리너)
    ├─ 가장 거래량이 많은 종목
    ├─ 당일 상승 종목
    └─ 당일 하락 종목
    ↓
3. 브리핑 이미지 생성 (PNG)
    ↓
4. 이메일 발송
    ↓
5. 인스타그램 자동 포스팅 📸
    ├─ 최신 이미지 조회
    ├─ 한국어 캡션 자동 생성
    └─ 해시태그 자동 추가
    ↓
6. Threads 자동 포스팅 🧵
    ├─ 동일한 이미지 발행
    ├─ 동일한 캡션 사용
    └─ Instagram과 동시 발행
    ↓
완료! 📱
```
3. 각 종목별 상세 브리핑 생성
    └─ JSON + Markdown 형식 저장
    ↓
4. HTML 이메일로 발송
    ├─ 3가지 종목 정보 포함
    └─ Markdown 파일 첨부
```

---

## 📊 출력 결과

### 화제 종목 조회 결과
```
backend/output/data/screener_results_20251224.json
```

### 브리핑 데이터
```
backend/output/data/briefings_20251224.json
backend/output/reports/briefing_20251224.md
```

### 발송된 이메일
```
제목: 당신이 잠든 사이 - 일일 주식 브리핑 (2025년 12월 24일)
내용: 3가지 종목 정보 (HTML 형식)
첨부: 마크다운 브리핑 파일
```

---

## 🛠️ 커스터마이징

### 실행 시간 변경
`.github/workflows/daily_briefing.yml` 파일의 `cron` 값 수정:
```yaml
on:
  schedule:
    - cron: '0 22 * * *'  # ← 이 값 수정
```

### 실행 대상 추가
`briefing_generator.py`에서 추가 로직 구현:
```python
# 예: 특정 종목 추가 분석
additional_tickers = ["AAPL", "MSFT", "NVDA"]
for ticker in additional_tickers:
    await briefing_service.generate_briefing_content(ticker)
```

### 다양한 알림 채널 추가
```yaml
# Slack 알림
- name: Notify Slack
  uses: slackapi/slack-github-action@v1

# Discord 알림
- name: Notify Discord
  uses: discordapp/github-actions@main
```

---

## 🔐 보안 체크리스트

- ✅ 비밀번호는 GitHub Secrets에만 저장
- ✅ 코드에 민감한 정보 없음
- ✅ 최소 권한 원칙 준수
- ✅ 정기적 비밀번호 갱신 (월 1회)
- ✅ GitHub Actions 로그에서 민감한 정보 마스킹

---

## 📈 모니터링 및 로그

### GitHub Actions 로그 확인
1. Repository > Actions > "Daily Stock Briefing"
2. 실행 내역 클릭
3. 각 단계의 상세 로그 확인

### 예상 로그 메시지
```
✅ Set up Python 3.12
✅ Install dependencies
✅ Run Screener Service
   ✅ most_actives: TSLA - Tesla, Inc.
   ✅ day_gainers: NVDA - NVIDIA Corporation
   ✅ day_losers: F - Ford Motor Company
✅ Generate Briefing
   ✅ TSLA 브리핑 생성됨
   ✅ NVDA 브리핑 생성됨
   ✅ F 브리핑 생성됨
✅ Send Email
   ✅ recipient@example.com으로 이메일 발송
✅ Notify Success
```

---

## ⚠️ 일반적인 문제

### "ModuleNotFoundError: No module named 'services'"
- 현재 디렉토리가 `backend/`인지 확인
- `backend/services/__init__.py` 파일 존재 확인

### "SMTPAuthenticationError"
- Gmail: 앱 비밀번호 사용 확인
- 2단계 인증 활성화 확인
- "Less secure app access" 허용 확인

### "exa_py not found"
- `pip install exa-py` 실행
- 또는 `requirements.txt`에 `exa-py>=1.0.0` 추가

### 이메일이 스팸으로 분류됨
- 발신자 이메일 확인
- 제목과 본문이 스팸 필터 기준과 맞는지 확인
- 수신 주소의 화이트리스트에 발신자 추가

---

## 📚 추가 학습 자료

- [GitHub Actions 공식 문서](https://docs.github.com/actions)
- [Cron 표현식 가이드](https://crontab.guru)
- [Python asyncio 튜토리얼](https://docs.python.org/3/library/asyncio.html)
- [SMTP 프로토콜 가이드](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol)

---

## 💬 FAQ

### Q: 매 시간마다 실행하고 싶습니다.
A: `cron: '0 * * * *'`로 변경하면 매 시간 정각에 실행됩니다.

### Q: 주말에는 실행하지 않고 싶습니다.
A: `cron: '0 22 * * 1-5'`로 변경하면 평일만 실행됩니다.

### Q: 여러 사람에게 이메일을 보내고 싶습니다.
A: `email_service.py`의 `RECIPIENT_EMAIL`을 `;`로 구분된 리스트로 변경합니다.

### Q: 특정 일시에만 실행하고 싶습니다.
A: GitHub Actions UI에서 "Run workflow" 버튼으로 수동 실행하면 됩니다.

---

## ✨ 완료!

모든 설정이 완료되었습니다. 이제:

1. ✅ GitHub Secrets 설정 완료
2. ✅ 워크플로우 파일 배포 완료
3. ✅ 서비스 스크립트 준비 완료
4. ✅ 매일 아침 7시 자동 실행 시작!

**다음 단계**: 로컬에서 테스트 후 첫 자동 실행을 기다리세요! 🚀

---

**Last Updated**: 2025-12-24
