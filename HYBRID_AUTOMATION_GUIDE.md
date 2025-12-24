# 🚀 하이브리드 자동화 설정 가이드

## 📋 새로운 아키텍처

GitHub Actions의 IP 블랙리스트 문제를 해결하기 위해 **하이브리드 구조**로 변경했습니다:

### 🌍 클라우드 (GitHub Actions) - 07:00 AM KST
```
GitHub Actions
├─ 화제 종목 조회 (Yahoo Finance)
├─ 브리핑 이미지 생성
└─ GitHub 저장소에 자동 커밋
```

### 💻 로컬 (Windows Task Scheduler) - 07:10 AM KST
```
Windows Task Scheduler
└─ 생성된 브리핑 이미지를 Instagram에 포스팅
```

**장점:**
- ✅ GitHub Actions IP 블랙리스트 문제 해결
- ✅ 개인 컴퓨터의 신뢰할 수 있는 IP에서 Instagram 포스팅
- ✅ 두 시스템 모두 자동화
- ✅ 장애 격리 (한 시스템 실패 시 다른 시스템은 계속 실행)

---

## 🛠️ 설정 방법 (3단계)

### 1️⃣ Windows Task Scheduler 설정 (1회만)

#### 옵션 A: PowerShell 스크립트 자동 설정

```powershell
# 관리자 권한으로 실행
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
.\setup_instagram_scheduler.ps1
```

#### 옵션 B: 수동 설정

1. **작업 스케줄러** 열기 (Windows + R → `taskschd.msc`)
2. **작업 만들기**
3. **일반** 탭:
   - 이름: `Instagram Daily Posting`
   - 설명: `Post daily briefing to Instagram`
   - ☑ 사용자가 로그인하지 않아도 실행

4. **트리거** 탭:
   - **새로 만들기** → 일정
   - **반복**: 매일
   - **시간**: 07:10 AM (GitHub Actions 07:00 실행 후 10분)
   - **반복 간격**: 매일

5. **작업** 탭:
   - **새로 만들기**
   - **프로그램/스크립트**: `C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\post_instagram.bat`
   - **시작 위치**: `C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard`

6. **확인** 클릭

### 2️⃣ GitHub Actions 확인

1. GitHub 저장소 → **Actions 탭**
2. **Daily Stock Briefing with Instagram Posting** 선택
3. 매일 **07:00 AM (KST)**에 자동 실행됨
4. 데이터 수집 + 이미지 생성 완료
5. GitHub 저장소에 자동 커밋됨

### 3️⃣ 로컬 Task Scheduler 확인

1. **작업 스케줄러** 열기
2. **작업 라이브러리** → `Instagram Daily Posting` 선택
3. 매일 **07:10 AM**에 자동 실행됨
4. `logs/instagram_posting.log`에 실행 로그 저장됨

---

## 🧪 테스트 방법

### 즉시 테스트 (GitHub Actions)

```
1. GitHub 저장소 → Actions 탭
2. "Daily Stock Briefing with Instagram Posting" 선택
3. "Run workflow" 클릭
4. 5분 후 완료 확인
```

### 즉시 테스트 (로컬 Instagram 포스팅)

**Terminal에서:**

```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
.\post_instagram.bat
```

**또는 로그 확인:**

```powershell
Get-Content logs\instagram_posting.log -Tail 50
```

---

## 📊 실행 일정

### 매일 아침 자동 실행

```
07:00 AM (KST) - GitHub Actions 시작
  ├─ 화제 종목 조회
  ├─ 브리핑 이미지 생성
  ├─ GitHub 커밋
  └─ 완료 (약 2-3분)

07:10 AM (KST) - Windows Task Scheduler 시작
  ├─ 최신 이미지 로드
  ├─ Instagram 로그인
  ├─ 이미지 + 캡션 포스팅
  └─ 완료 (약 1-2분)

결과: 매일 07:15 AM쯤 Instagram 프로필에 포스트 나타남
```

---

## 🔍 문제 해결

### ❌ Task Scheduler가 실행되지 않음

**원인**: 작업이 비활성화됨

**해결**:
1. 작업 스케줄러 열기
2. `Instagram Daily Posting` 우클릭
3. **활성화** 클릭

### ❌ Instagram 포스팅 실패

**원인**: 계정 정보 오류

**해결**:
```powershell
cd backend
python test_instagram_credentials.py
```

### ❌ 로그가 없음

**확인**:
```powershell
ls logs\
```

**로그 확인**:
```powershell
Get-Content logs\instagram_posting.log
```

### ❌ GitHub Actions 실패

**로그 확인**:
1. GitHub 저장소 → Actions 탭
2. 실패한 워크플로우 클릭
3. 각 단계의 로그 확인

---

## 📱 Instagram 계정 정보

현재 설정된 계정:
- **사용자명**: `chocomadeline70@gmail.com`
- **비밀번호**: `google2022!` (backend/.env에 저장)

변경 시:
```bash
# backend/.env 수정
INSTAGRAM_USERNAME=new_username
INSTAGRAM_PASSWORD=new_password
```

---

## 🎯 일일 체크리스트

매일 아침 체크:

```
[ ] 07:00 AM: GitHub Actions 시작 확인
    → GitHub Actions 탭 확인

[ ] 07:15 AM: Instagram 프로필 확인
    → 새 포스트 나타났는지 확인

[ ] 로그 확인
    → logs/instagram_posting.log 확인

[ ] 문제 발생 시
    → 위의 문제 해결 가이드 참조
```

---

## 💡 팁

### 수동 실행하기

```powershell
# GitHub Actions 데이터 생성
cd backend
python -m services.screener_service
python -m services.briefing_generator

# Instagram 포스팅
python -m services.instagram_service
```

### 로그 실시간 모니터링

```powershell
Get-Content logs\instagram_posting.log -Wait
```

### 시간대 변경하기

**GitHub Actions 시간 변경** (`.github/workflows/daily_briefing_instagram.yml`):
```yaml
cron: '0 22 * * *'  # UTC 22:00 = KST 07:00
# 변경 예: cron: '0 0 * * *'  # UTC 00:00 = KST 09:00
```

**Task Scheduler 시간 변경** (작업 스케줄러):
1. `Instagram Daily Posting` 우클릭
2. **속성** → **트리거** 탭
3. 시간 수정

---

## ✅ 완성!

```
✅ GitHub Actions: 매일 07:00 AM에 데이터 생성
✅ Windows Task Scheduler: 매일 07:10 AM에 Instagram 포스팅
✅ 완전 자동화된 "While You Were Sleeping" 시스템 구축 완료!
```

---

## 📞 추가 지원

문제가 있으면:

1. 로그 확인: `logs/instagram_posting.log`
2. GitHub Actions 로그 확인
3. 계정 정보 검증: `python test_instagram_credentials.py`
4. 수동 실행으로 테스트: `python -m services.instagram_service`

🚀 **이제 완전 자동화되었습니다!**
