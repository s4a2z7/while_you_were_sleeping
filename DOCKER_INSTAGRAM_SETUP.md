# 🐳 Docker를 이용한 인스타그램 자동 게시

## ✨ 개요

Docker 컨테이너에서 별도로 `instagrapi`를 실행하여 **pydantic 버전 충돌 문제를 해결**합니다.

```
📊 FastAPI 백엔드 (pydantic 2.5.0+)
   ├─ 화제 종목 조회
   ├─ 브리핑 생성
   └─ 이메일 발송

🐳 Docker 컨테이너 (pydantic 1.10.2)
   └─ 📱 인스타그램 게시 ← 격리된 환경에서 실행!
```

---

## 🚀 빠른 시작 (3단계)

### Step 1: Docker 설치

**Windows:**
- [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) 다운로드
- 설치 후 재부팅
- PowerShell에서 확인:
  ```powershell
  docker --version
  ```

### Step 2: `.env` 파일 설정

프로젝트 루트에 `.env` 파일 생성:

```env
# 📱 인스타그램 설정
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_app_password

# 📧 이메일 설정 (기존)
SENDER_EMAIL=chocomadeline70@gmail.com
SENDER_PASSWORD=aktfmrnnrzpjfbke
RECIPIENT_EMAIL=chocomadeline70@gmail.com
```

### Step 3: Docker 이미지 빌드 및 실행

```powershell
# 1. 이미지 빌드 (첫 실행 시만)
docker build -f Dockerfile.instagram -t instagram-poster .

# 2. 컨테이너 실행 (테스트)
docker run --rm `
  -e INSTAGRAM_USERNAME=your_username `
  -e INSTAGRAM_PASSWORD=your_app_password `
  -v "$(Get-Location)\output\images:/app/output/images:ro" `
  -v "$(Get-Location)\output\data:/app/output/data:ro" `
  instagram-poster
```

---

## 📋 상세 사용법

### 방법 1: 직접 docker run (간단)

```powershell
# 테스트 실행
$env:INSTAGRAM_USERNAME="your_username"
$env:INSTAGRAM_PASSWORD="your_app_password"

docker run --rm `
  -e INSTAGRAM_USERNAME=$env:INSTAGRAM_USERNAME `
  -e INSTAGRAM_PASSWORD=$env:INSTAGRAM_PASSWORD `
  -v "$(Get-Location)\output\images:/app/output/images:ro" `
  -v "$(Get-Location)\output\data:/app/output/data:ro" `
  instagram-poster
```

### 방법 2: docker-compose (권장)

```powershell
# 1. 이미지 빌드
docker-compose -f docker-compose.instagram.yml build

# 2. 컨테이너 실행
docker-compose -f docker-compose.instagram.yml up

# 3. 백그라운드에서 실행
docker-compose -f docker-compose.instagram.yml up -d

# 4. 로그 확인
docker-compose -f docker-compose.instagram.yml logs -f

# 5. 정지
docker-compose -f docker-compose.instagram.yml down
```

### 방법 3: Windows Task Scheduler와 함께 사용

Task Scheduler에 다음 PowerShell 스크립트로 등록:

```powershell
# run_instagram_docker.ps1
$env:INSTAGRAM_USERNAME="your_username"
$env:INSTAGRAM_PASSWORD="your_app_password"

docker run --rm `
  -e INSTAGRAM_USERNAME=$env:INSTAGRAM_USERNAME `
  -e INSTAGRAM_PASSWORD=$env:INSTAGRAM_PASSWORD `
  -v "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\output\images:/app/output/images:ro" `
  -v "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\output\data:/app/output/data:ro" `
  instagram-poster

Write-Host "인스타그램 게시 완료" -ForegroundColor Green
```

---

## 🐳 Docker 명령어

### 이미지 관리

```powershell
# 이미지 빌드
docker build -f Dockerfile.instagram -t instagram-poster .

# 이미지 목록 확인
docker images | Select-String instagram-poster

# 이미지 삭제
docker rmi instagram-poster
```

### 컨테이너 관리

```powershell
# 실행 중인 컨테이너 확인
docker ps

# 모든 컨테이너 확인
docker ps -a

# 로그 확인
docker logs [container_id]

# 실시간 로그
docker logs -f [container_id]

# 컨테이너 정지
docker stop [container_id]

# 컨테이너 재시작
docker restart [container_id]
```

---

## 🔍 문제 해결

### "Docker daemon is not running"

```powershell
# Docker Desktop 시작
# 또는 cmd에서:
docker-machine start
```

### "Cannot find image" 오류

```powershell
# 이미지 다시 빌드
docker build -f Dockerfile.instagram -t instagram-poster .
```

### "Permission denied" 오류

PowerShell을 **관리자 권한**으로 실행하세요.

### 볼륨 마운트 오류 (Windows)

경로를 다음과 같이 수정:

```powershell
# ❌ 틀린 예
-v "C:\path\to\files:/app/files"

# ✅ 올바른 예 (PowerShell)
-v "$(Get-Location)\output\images:/app/output/images:ro"

# ✅ 또는 (cmd)
-v "%CD%\output\images:/app/output/images:ro"
```

---

## 📊 구조

```
프로젝트/
├── Dockerfile.instagram          ← 인스타그램 컨테이너 설정
├── docker-compose.instagram.yml  ← docker-compose 설정
├── backend/
│   ├── requirements_instagram.txt ← instagrapi 의존성
│   ├── services/
│   │   └── instagram_service.py   ← 인스타그램 서비스
│   └── .env                       ← 계정 정보 (gitignore)
├── output/
│   ├── images/                    ← 브리핑 이미지 (Docker에서 읽음)
│   └── data/                      ← 주식 데이터 (Docker에서 읽음)
└── run_instagram_docker.ps1       ← Task Scheduler용 스크립트
```

---

## 🎯 자동화 설정

### Windows Task Scheduler에 등록

1. **PowerShell 스크립트 생성** (`run_instagram_docker.ps1`)

```powershell
$env:INSTAGRAM_USERNAME="your_username"
$env:INSTAGRAM_PASSWORD="your_app_password"

docker run --rm `
  -e INSTAGRAM_USERNAME=$env:INSTAGRAM_USERNAME `
  -e INSTAGRAM_PASSWORD=$env:INSTAGRAM_PASSWORD `
  -v "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\output\images:/app/output/images:ro" `
  -v "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\output\data:/app/output/data:ro" `
  instagram-poster
```

2. **Task Scheduler 작업 생성**

```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At 7:30AM  # 07:30 (브리핑 생성 후)
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-ExecutionPolicy Bypass -File C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\run_instagram_docker.ps1"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -TaskName "Instagram Auto-Poster" `
  -Trigger $trigger `
  -Action $action `
  -Settings $settings `
  -Principal $principal `
  -Description "매일 07:30 AM에 인스타그램에 자동 게시" `
  -Force
```

---

## 📈 완성된 자동화

```
📅 매일 시간별 실행:

07:00 AM ── Windows Task Scheduler
   ├─ run_daily_briefing.py (메인 파이프라인)
   │  ├─ [1/5] 화제 종목 조회
   │  ├─ [2/5] 브리핑 생성 (이미지 생성)
   │  ├─ [3/5] 📧 이메일 발송
   │  └─ output/ 폴더 채움
   │
   └─ (output 기다림)

07:30 AM ── Docker 컨테이너
   └─ run_instagram_docker.ps1
      └─ 📱 인스타그램 게시 (output에서 이미지 읽음)
```

---

## 💡 팁

### 로그 저장

```powershell
# 컨테이너 실행 시 로그 저장
docker run --rm `
  -e INSTAGRAM_USERNAME=$env:INSTAGRAM_USERNAME `
  -e INSTAGRAM_PASSWORD=$env:INSTAGRAM_PASSWORD `
  -v "$(Get-Location)\output:/app/output:ro" `
  instagram-poster > instagram_$(Get-Date -Format 'yyyyMMdd_HHmmss').log 2>&1
```

### 이미지 최적화

```dockerfile
# Dockerfile.instagram의 베이스 이미지 변경
FROM python:3.12-slim  # 작은 크기 (~200MB)
# 또는
FROM python:3.12       # 전체 기능 (~900MB)
```

### 캐시 사용

```powershell
# 빠른 재빌드 (캐시 사용)
docker build -f Dockerfile.instagram -t instagram-poster .

# 캐시 무시 (완전 재빌드)
docker build --no-cache -f Dockerfile.instagram -t instagram-poster .
```

---

## ✅ 체크리스트

- [ ] Docker Desktop 설치 및 실행
- [ ] `.env` 파일에 INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD 설정
- [ ] 이미지 빌드: `docker build -f Dockerfile.instagram -t instagram-poster .`
- [ ] 테스트 실행: `docker run --rm ... instagram-poster`
- [ ] Instagram 프로필 확인 (새 포스트 확인)
- [ ] Task Scheduler에 `run_instagram_docker.ps1` 등록
- [ ] 매일 07:30 AM 자동 실행 확인

---

**이제 Docker로 깔끔하게 인스타그램 자동 게시를 관리할 수 있습니다! 🐳📱**
