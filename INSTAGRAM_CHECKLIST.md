# 📱 인스타그램 자동 게시 - 실행 체크리스트

## ✅ 체크리스트 (5분 내 완료)

### 1️⃣ Instagram 앱 비밀번호 준비
- [ ] Instagram 계정 접속 (instagram.com 또는 앱)
- [ ] 설정 → 보안 → 앱 비밀번호 생성
- [ ] 16자리 비밀번호 복사 (예: `abcd1234efgh5678`)

### 2️⃣ `.env` 파일 수정
- [ ] `backend/.env` 파일 열기
- [ ] 다음 2줄 추가:
  ```
  INSTAGRAM_USERNAME=your_username
  INSTAGRAM_PASSWORD=abcd1234efgh5678
  ```
- [ ] 파일 저장

### 3️⃣ instagrapi 설치
- [ ] PowerShell 열기
- [ ] 명령 실행:
  ```powershell
  cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
  python -m venv insta_env
  insta_env\Scripts\Activate.ps1
  pip install -r backend\requirements_instagram.txt
  ```
- [ ] 설치 완료 확인

### 4️⃣ 테스트 실행
- [ ] 명령 실행:
  ```powershell
  cd backend
  python test_instagram_setup.py
  ```
- [ ] "✅ 모든 테스트 성공!" 메시지 확인

### 5️⃣ 첫 게시 테스트
- [ ] 명령 실행:
  ```powershell
  python -m services.instagram_service
  ```
- [ ] Instagram 프로필 확인 (새 포스트 등록됨)

---

## 🎯 자동 실행 설정

**이미 Task Scheduler에 설정되어 있습니다:**

```
📅 매일 07:00 AM 자동 실행
├─ 화제 종목 조회
├─ 브리핑 생성
├─ 📧 이메일 발송
├─ 📱 인스타그램 게시 ← 자동 포함!
└─ 🧵 Threads 게시 ← 자동 포함!
```

**Task Scheduler 작업 확인:**
```powershell
Get-ScheduledTask -TaskName "Daily Stock Briefing"
```

---

## 🔍 문제 해결

### ❌ "BadPassword" 오류

**원인**: 일반 비밀번호 사용

**해결**:
1. Instagram 앱 비밀번호 (일반 비밀번호 아님) 사용
2. 2단계 인증 활성화 확인
3. 계정 잠금 해제

### ❌ "No module named 'instagrapi'"

**원인**: instagrapi 미설치

**해결**:
```powershell
pip install -r backend\requirements_instagram.txt
```

### ❌ "이미지를 찾을 수 없습니다"

**원인**: 브리핑이 먼저 생성되어야 함

**해결**:
```powershell
cd backend
python -m services.briefing_generator
```

---

## 📝 파일 위치

| 항목 | 경로 |
|------|------|
| 설정 파일 | `backend/.env` |
| 인스타그램 서비스 | `backend/services/instagram_service.py` |
| 자동화 스크립트 | `run_daily_briefing.py` |
| 테스트 스크립트 | `backend/test_instagram_setup.py` |
| 의존성 파일 | `backend/requirements_instagram.txt` |
| 생성된 포스트 | `output/images/briefing_card_*.png` |

---

## 🚀 명령어 정리

```powershell
# 가상 환경 활성화
insta_env\Scripts\Activate.ps1

# instagrapi 설치
pip install -r backend\requirements_instagram.txt

# 테스트 실행
cd backend
python test_instagram_setup.py

# 인스타그램 게시 (수동)
python -m services.instagram_service

# 전체 파이프라인 (수동)
cd ..
python run_daily_briefing.py

# 가상 환경 비활성화
deactivate

# Task Scheduler 확인
Get-ScheduledTask -TaskName "Daily Stock Briefing"
```

---

## ✨ 생성되는 포스트 예시

```
📈 2025년 12월 25일 주식 브리핑

🔥 거래량 많은 종목
1. NVDA $140.50 +2.50%
2. TSLA $250.25 -1.25%

📈 오늘의 상승 종목
1. AAPL $195.30 +3.20%
2. AMZN $185.50 +2.10%

📉 오늘의 하락 종목
1. AMD $220.00 -2.50%
2. INTEL $45.75 -1.20%

#주식 #투자 #트렌드주
[+ 그래프 이미지]
```

---

**설정 완료 후 매일 07:00 AM에 자동 게시됩니다!** 🎉
