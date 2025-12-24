# 📱 인스타그램 자동 발송 설정 가이드

## ✨ 기능

매일 자동으로 생성된 주식 브리핑을 **인스타그램**에 발송합니다:

- ✅ 주식 그래프 이미지 업로드
- ✅ 자동 캡션 생성 (종목명, 가격, 변동률)
- ✅ 해시태그 자동 추가
- ✅ 일일 자동 실행

---

## 🔧 설정 방법

### Step 1: 인스타그램 앱 비밀번호 생성

**작업 계정용 Instagram Business Account 추천:**

1. **Instagram 앱 열기** (모바일 또는 웹)
2. **프로필 → 설정 및 개인정보 보호**
3. **보안**
4. **앱 비밀번호** (또는 "App Password")
5. **새 앱 비밀번호 생성**
   - 앱: "Other"
   - 기기: "Windows"
6. **16자리 비밀번호** 복사

**또는 2단계 인증 계정의 경우:**

1. Facebook 계정 설정 (instagram.com → 설정)
2. 2단계 인증 활성화
3. 앱 비밀번호 생성

---

### Step 2: `.env` 파일 설정

프로젝트의 `backend/.env` 파일에 다음을 추가하세요:

```env
# 📧 이메일 설정 (기존)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com

# 📱 인스타그램 설정 (새로 추가)
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_app_password
```

**예시:**
```env
INSTAGRAM_USERNAME=stock_briefing_bot
INSTAGRAM_PASSWORD=abcd1234efgh5678
```

---

### Step 3: instagrapi 설치

**주의:** pydantic 버전 충돌이 있으므로 별도의 환경에서 설치해야 합니다.

#### 옵션 A: 전용 가상 환경 생성 (권장)

```powershell
# 1. 프로젝트 루트로 이동
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"

# 2. 새 가상 환경 생성
python -m venv insta_env

# 3. 가상 환경 활성화
insta_env\Scripts\Activate.ps1

# 4. instagrapi 설치
pip install instagrapi==2.0.0

# 5. 비활성화
deactivate
```

#### 옵션 B: Docker 컨테이너 사용

```dockerfile
FROM python:3.12
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements_instagram.txt
CMD ["python", "-m", "services.instagram_service"]
```

#### 옵션 C: 별도 요구사항 파일

`backend/requirements_instagram.txt` 생성:
```
pydantic==1.10.2
instagrapi==2.0.0
python-dotenv>=1.0.0
pillow>=10.0.0
```

---

## 📋 사용 방법

### 방법 1: 일일 자동 실행 (권장)

Task Scheduler 설정 시 자동으로 실행됩니다:

```
매일 07:00 AM
1. 화제 종목 조회
2. 브리핑 생성
3. 이메일 발송
4. 인스타그램 발송 ← 자동 포함!
```

### 방법 2: 수동 테스트

**PowerShell에서 직접 실행:**

```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\backend"
python -m services.instagram_service
```

**로그 확인:**
```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" -Tail 30
```

---

## 📸 생성되는 콘텐츠

### 인스타그램 포스트 예시:

```
📈 2025년 12월 25일 주식 브리핑

🔥 거래량 많은 종목
1. NVDA $140.50 +2.50%
2. TSLA $250.25 -1.25%
3. MSFT $430.75 +1.75%

📈 오늘의 상승 종목
1. AAPL $195.30 +3.20%
2. AMZN $185.50 +2.10%
3. META $500.00 +1.80%

📉 오늘의 하락 종목
1. AMD $220.00 -2.50%
2. INTEL $45.75 -1.20%
3. QUALCOMM $180.25 -0.50%

#주식 #투자 #트렌드주 #화제종목 #주식시장 #주식정보
```

**포함 내용:**
- ✅ 브리핑 날짜
- ✅ 거래량 많은 종목 TOP 3
- ✅ 상승 종목 TOP 3
- ✅ 하락 종목 TOP 3
- ✅ 관련 해시태그
- ✅ 생성된 그래프 이미지

---

## 🔍 문제 해결

### 로그인 실패

**오류: "Bad password / 로그인 실패"**

1. ✅ Instagram 앱 비밀번호 확인 (일반 비밀번호 아님)
2. ✅ 계정이 2단계 인증 활성화되었는지 확인
3. ✅ 계정이 잠겨있지 않은지 확인
4. ✅ IP 차단이 아닌지 확인 (VPN 시도)

### 이미지를 찾을 수 없음

**오류: "브리핑 이미지를 찾을 수 없습니다"**

```powershell
# 이미지 폴더 확인
Get-ChildItem "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\output\images"

# 브리핑 생성이 완료되었는지 확인
Get-ChildItem "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\output\data"
```

### 캡션 생성 오류

**오류: "캡션 생성 오류"**

1. ✅ 스크리너 데이터가 존재하는지 확인
2. ✅ JSON 파일 형식이 올바른지 확인
3. ✅ 주식 데이터에 필수 필드 확인 (symbol, price, change_percent)

---

## 📊 로그 파일 확인

### 실시간 모니터링

```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" -Wait
```

### 최근 인스타그램 관련 로그

```powershell
Get-Content "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\briefing_scheduler.log" | Select-String "인스타그램|instagram|Instagram" -CaseSensitive
```

---

## 🛡️ 보안 주의사항

### ⚠️ 중요:

1. **`.env` 파일을 절대 공유하지 마세요**
   - GitHub에 커밋하지 않기
   - `.gitignore`에 포함되어 있는지 확인

2. **앱 비밀번호 사용**
   - 일반 비밀번호 사용 금지
   - 정기적으로 비밀번호 변경

3. **권한 최소화**
   - 봇용 별도 계정 추천
   - 중요 계정에는 사용 금지

### .gitignore 확인

```
backend/.env
backend/.env.local
insta_env/
__pycache__/
*.pyc
```

---

## 🚀 다음 단계

### 자동 실행 설정

```powershell
# 1. 관리자 PowerShell 열기
# 2. Task Scheduler 설정 실행
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\setup_task_scheduler.ps1
```

### 수동 테스트

```powershell
# 1. 전체 파이프라인 테스트
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
python run_daily_briefing.py

# 2. 로그 확인
Get-Content "briefing_scheduler.log" -Tail 50
```

---

## 📞 지원

### 설정 도움말

1. [QUICK_START_SCHEDULER.md](QUICK_START_SCHEDULER.md) - 빠른 시작 가이드
2. [TASK_SCHEDULER_SETUP.md](TASK_SCHEDULER_SETUP.md) - Task Scheduler 상세 가이드
3. [ADMIN_SETUP_GUIDE.md](ADMIN_SETUP_GUIDE.md) - 관리자 권한 설정

### API 문서

- [instagrapi 문서](https://github.com/subzeroid/instagrapi)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-graph-api)

---

**이제 매일 자동으로 인스타그램에 주식 브리핑이 발송됩니다! 🎉**
