# 📱 인스타그램 자동 게시 완전 가이드

## ✨ 완성된 기능

**다음이 매일 자동으로 실행됩니다:**

```
📅 매일 07:00 AM
├─ [1/5] 화제 종목 조회 ✅
├─ [2/5] 브리핑 생성 ✅
├─ [3/5] 📧 이메일 발송 ✅
├─ [4/5] 📱 인스타그램 게시 ✅ (새로 추가!)
└─ [5/5] 🧵 Threads 게시 ✅ (새로 추가!)
```

---

## 🚀 빠른 시작 (5분)

### Step 1: `.env` 파일 수정

`backend/.env`를 열어서 다음을 추가하세요:

```env
# 📧 이메일 (기존)
SENDER_EMAIL=chocomadeline70@gmail.com
SENDER_PASSWORD=aktfmrnnrzpjfbke
RECIPIENT_EMAIL=chocomadeline70@gmail.com

# 📱 인스타그램 + Threads (새로 추가)
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_app_password
```

**예시:**
```env
INSTAGRAM_USERNAME=stock_briefing_bot
INSTAGRAM_PASSWORD=abcd1234efgh5678
```

### Step 2: 인스타그램 앱 비밀번호 생성

**중요: 일반 비밀번호가 아닌 앱 비밀번호를 사용해야 합니다!**

1. **Instagram 앱 또는 웹** (instagram.com) 열기
2. **프로필 → 설정 및 개인정보 보호**
3. **보안** → **앱 비밀번호** (또는 "App Password")
4. **새 앱 비밀번호** 생성
   - 앱: "기타" (Other)
   - 기기: "Windows"
5. **16자리 비밀번호** 복사 → `.env`에 붙여넣기

### Step 3: instagrapi 설치

**이 단계가 가장 중요합니다!** (pydantic 버전 충돌이 있습니다)

#### 옵션 A: 별도 가상 환경 사용 (권장) ⭐

```powershell
# 1. 프로젝트 루트로 이동
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"

# 2. 새 가상 환경 생성
python -m venv insta_env

# 3. 활성화
insta_env\Scripts\Activate.ps1

# 4. 의존성 설치
pip install -r backend\requirements_instagram.txt

# 5. 테스트 실행
cd backend
python test_instagram_setup.py

# 6. 비활성화 (작업 완료 후)
deactivate
```

#### 옵션 B: Docker 사용

```dockerfile
FROM python:3.12
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements_instagram.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "services.instagram_service"]
```

#### 옵션 C: 현재 환경에 설치 (비추천)

```powershell
pip install instagrapi==2.0.0 --force-reinstall --no-deps
```

### Step 4: 테스트

```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\backend"
python test_instagram_setup.py
```

**성공하면 다음과 같이 표시됩니다:**

```
✅ Step 1: 환경변수 확인
   ✅ 사용자명: your_username
   ✅ 앱 비밀번호: ****

✅ Step 2: instagrapi 설치 확인
   ✅ instagrapi 설치됨 (v2.0.0)

✅ Step 3: 인스타그램 서비스 로드
   ✅ InstagramService 로드 성공

✅ Step 4: 인스타그램 로그인 테스트
   ✅ 로그인 성공!

✅ 모든 테스트 성공! 인스타그램 준비 완료
```

---

## 🎯 즉시 테스트

### 방법 1: 인스타그램만 게시

```powershell
cd backend
python -m services.instagram_service
```

### 방법 2: 전체 파이프라인 (이메일 + 인스타그램 + Threads)

```powershell
cd ..
python run_daily_briefing.py
```

### 방법 3: Task Scheduler 자동 실행

기존 설정 유지 (이미 `run_daily_briefing.py`를 실행하므로 자동 포함)

```powershell
# Task Scheduler 작업 확인
Get-ScheduledTask -TaskName "Daily Stock Briefing"
```

---

## 📊 자동 게시 내용 예시

### 인스타그램 포스트

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

#주식 #투자 #트렌드주 #화제종목 
#주식시장 #주식정보 #데이트레이딩
```

**포함 내용:**
- ✅ 브리핑 날짜
- ✅ 거래량 많은 종목 TOP 3
- ✅ 상승 종목 TOP 3
- ✅ 하락 종목 TOP 3
- ✅ 생성된 그래프 이미지
- ✅ 관련 해시태그

---

## 🔧 문제 해결

### "Bad password" 오류

```
❌ 로그인 실패
   • 사용자명 확인: INSTAGRAM_USERNAME
   • 앱 비밀번호 확인: INSTAGRAM_PASSWORD
```

**해결:**
1. ✅ 일반 비밀번호가 아닌 **앱 비밀번호** 확인
2. ✅ 2단계 인증 활성화 확인
3. ✅ 계정이 잠겨있지 않은지 확인
4. ✅ Instagram 앱에서 로그아웃 후 재시도

### "이미지를 찾을 수 없음" 오류

```
⚠️  이미지를 찾을 수 없습니다
```

**해결:**
먼저 브리핑을 생성하세요:

```powershell
cd backend
python -m services.briefing_generator
```

### "주식 데이터를 찾을 수 없음" 오류

```
⚠️  주식 데이터를 찾을 수 없습니다
```

**해결:**
먼저 스크리너를 실행하세요:

```powershell
cd backend
python -m services.screener_service
```

### instagrapi 설치 오류

```
ModuleNotFoundError: No module named 'instagrapi'
```

**해결:**
위의 "Step 3: instagrapi 설치" 섹션을 따라하세요. **별도 가상 환경 사용을 권장합니다.**

---

## 📋 파일 설명

| 파일 | 역할 |
|------|------|
| `services/instagram_service.py` | 인스타그램 게시 로직 |
| `services/threads_service.py` | Threads 게시 로직 |
| `run_daily_briefing.py` | 5단계 자동화 파이프라인 |
| `backend/requirements_instagram.txt` | instagrapi 전용 의존성 |
| `test_instagram_setup.py` | 설정 테스트 스크립트 |
| `backend/.env` | 계정 정보 (git에서 제외) |

---

## 🛡️ 보안 주의

### ⚠️ 중요 사항

1. **`.env` 파일을 절대 GitHub에 커밋하지 마세요!**
   ```
   # .gitignore 확인
   backend/.env ✅ 포함되어 있어야 함
   ```

2. **앱 비밀번호 사용 필수**
   - 일반 비밀번호 사용 금지
   - 2단계 인증 활성화

3. **봇용 별도 계정 추천**
   - 개인 계정 사용 금지
   - 비즈니스 계정 권장

---

## 🚀 다음 단계

### 설정 완료 후

```powershell
# 1. Task Scheduler 확인
Get-ScheduledTask -TaskName "Daily Stock Briefing"

# 2. 내일 07:00 AM 대기
# 또는 수동 테스트

# 3. 인스타그램 확인
# @your_instagram_username 프로필에서 새 포스트 확인
```

### 모니터링

```powershell
# 실시간 로그 보기
Get-Content "briefing_scheduler.log" -Wait

# 최근 로그만 보기
Get-Content "briefing_scheduler.log" -Tail 30
```

---

## 📞 지원

### 가이드 문서
- [QUICK_START_SCHEDULER.md](QUICK_START_SCHEDULER.md) - Task Scheduler 빠른 시작
- [ADMIN_SETUP_GUIDE.md](ADMIN_SETUP_GUIDE.md) - 관리자 권한 설정
- [INSTAGRAM_SETUP.md](INSTAGRAM_SETUP.md) - 이전 문서 (현재 파일)

### 유용한 명령어

```powershell
# 브리핑 생성
python -m services.briefing_generator

# 스크리너 실행
python -m services.screener_service

# 이메일 테스트
python test_send_email.py

# 인스타그램 테스트
python test_instagram_setup.py

# 전체 파이프라인
python run_daily_briefing.py
```

---

**이제 매일 자동으로 인스타그램에 주식 브리핑이 게시됩니다! 🎉**

**다음 실행: 내일 07:00 AM** ⏰
