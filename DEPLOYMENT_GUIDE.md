# 🚀 인스타그램 자동 게시 배포 완료!

## ✨ 준비된 것

```
✅ .env 설정
   INSTAGRAM_USERNAME=s4a2z7
   INSTAGRAM_PASSWORD=claude2022!

✅ Docker 이미지
   Dockerfile.instagram

✅ 자동 실행 스크립트
   run_instagram_docker.ps1
   deploy_instagram.ps1

✅ Task Scheduler 설정
   매일 07:30 AM 자동 게시
```

---

## 🎯 배포 3단계

### Step 1️⃣: Docker Desktop 실행

- Windows 시작 메뉴에서 "Docker Desktop" 검색
- 실행하고 **완전히 시작될 때까지 대기** (약 1-2분)
- 우측 하단 시스템 트레이에 Docker 아이콘 확인

### Step 2️⃣: 배포 스크립트 실행

PowerShell에서:

```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
.\deploy_instagram.ps1
```

**완료되면:**
```
================================
✅ 배포 완료!
================================
```

### Step 3️⃣: 자동 실행 설정

```powershell
# 관리자 PowerShell에서
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force

# Task Scheduler에 등록
$trigger = New-ScheduledTaskTrigger -Daily -At 7:30AM
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-ExecutionPolicy Bypass -File $(Get-Location)\run_instagram_docker.ps1"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -TaskName "Instagram Auto-Poster" `
  -Trigger $trigger `
  -Action $action `
  -Principal $principal `
  -Description "매일 07:30 AM에 주식 브리핑을 인스타그램에 게시" `
  -Force

Write-Host "✅ Task Scheduler 등록 완료!" -ForegroundColor Green
```

---

## ▶️ 즉시 테스트

배포 후 바로 테스트:

```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
.\run_instagram_docker.ps1
```

**성공 메시지:**
```
================================
✅ 인스타그램 게시 성공!
================================
   • 프로필에서 새 포스트 확인
```

---

## 📊 자동화 흐름

```
📅 매일 07:00 AM
↓
[Windows Task Scheduler]
↓
[run_daily_briefing.py]
├─ 화제 종목 조회
├─ 브리핑 생성 (이미지)
├─ 📧 이메일 발송
└─ output/ 폴더에 저장

📅 매일 07:30 AM
↓
[Windows Task Scheduler]
↓
[run_instagram_docker.ps1]
├─ Docker 컨테이너 시작
├─ output/ 폴더에서 이미지 읽음
└─ 📱 인스타그램에 게시
```

---

## 🔍 확인 방법

### 1. Task Scheduler 확인

```powershell
# 작업 목록
Get-ScheduledTask -TaskName "Instagram Auto-Poster"

# 실행 이력
Get-ScheduledTaskInfo -TaskName "Instagram Auto-Poster"
```

### 2. Instagram 프로필 확인

1. Instagram 앱 또는 웹 (instagram.com) 열기
2. 프로필 클릭
3. 최신 포스트 확인
4. 캡션: "📈 YYYY년 MM월 DD일 주식 브리핑"

### 3. 로그 확인

```powershell
# 최근 로그
docker logs --tail 20 [container_id]

# 실시간 로그
docker logs -f [container_id]
```

---

## 🛠️ 문제 해결

### ❌ "Docker daemon is not running"

→ Docker Desktop 재시작

### ❌ "Cannot find image"

→ `.\deploy_instagram.ps1` 다시 실행

### ❌ "Permission denied"

→ PowerShell을 **관리자 권한**으로 실행

### ❌ "Task not found"

→ Task Scheduler 설정 단계 다시 확인

### ❌ Instagram 프로필에 포스트 미표시

1. 인스타그램 로그인 확인 (다른 기기에서 비로그인될 수 있음)
2. `.env` 파일의 credentials 확인
3. `.\run_instagram_docker.ps1` 수동 실행 후 로그 확인

---

## 📚 참고 문서

- [DOCKER_INSTAGRAM_QUICK_START.md](DOCKER_INSTAGRAM_QUICK_START.md) - Docker 상세 가이드
- [DOCKER_INSTAGRAM_SETUP.md](DOCKER_INSTAGRAM_SETUP.md) - 전체 설명서
- [QUICK_START_SCHEDULER.md](QUICK_START_SCHEDULER.md) - Task Scheduler 설정

---

## ✅ 체크리스트

- [ ] Docker Desktop 설치 및 실행
- [ ] `.env` 파일에 Instagram 계정 설정
- [ ] `deploy_instagram.ps1` 실행 (Docker 이미지 빌드)
- [ ] `run_instagram_docker.ps1` 테스트 실행
- [ ] Instagram 프로필에서 포스트 확인
- [ ] Task Scheduler에 작업 등록
- [ ] 매일 07:30 AM 자동 실행 확인

---

## 🎉 완성!

```
📱 인스타그램 자동 게시 준비 완료!

매일:
✅ 07:00 AM - 화제 종목 조회 & 브리핑 생성
✅ 07:30 AM - 인스타그램에 자동 게시

🎯 목표 달성!
```

---

**문제가 있으면 로그를 확인하세요:**

```powershell
# Docker 로그
docker logs instagram-auto-poster

# PowerShell 로그
Get-Content "briefing_scheduler.log" -Tail 50
```
