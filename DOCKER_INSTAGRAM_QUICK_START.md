# 🐳 Docker 인스타그램 자동 게시 - 5분 가이드

## ⚡ 3단계로 완료

### Step 1️⃣: Docker Desktop 설치 (2분)

1. [Docker Desktop 다운로드](https://www.docker.com/products/docker-desktop)
2. 설치 및 재부팅
3. PowerShell에서 확인:
   ```powershell
   docker --version
   ```

### Step 2️⃣: 환경변수 설정 (1분)

프로젝트 루트의 `.env` 파일에 추가:

```env
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_app_password
```

### Step 3️⃣: 테스트 및 빌드 (2분)

```powershell
# 1. 프로젝트 폴더로 이동
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"

# 2. Docker 이미지 빌드
docker build -f Dockerfile.instagram -t instagram-poster .

# 3. 테스트 실행
$env:INSTAGRAM_USERNAME="your_username"
$env:INSTAGRAM_PASSWORD="your_app_password"

docker run --rm `
  -e INSTAGRAM_USERNAME=$env:INSTAGRAM_USERNAME `
  -e INSTAGRAM_PASSWORD=$env:INSTAGRAM_PASSWORD `
  -v "$(Get-Location)\output\images:/app/output/images:ro" `
  -v "$(Get-Location)\output\data:/app/output/data:ro" `
  instagram-poster
```

---

## ✅ 자동 실행 설정

### 방법 1: PowerShell 스크립트 (권장)

```powershell
# 1. 관리자 PowerShell 열기
# 2. 스크립트 실행 권한 설정
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force

# 3. Task Scheduler에 등록
$trigger = New-ScheduledTaskTrigger -Daily -At 7:30AM
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-ExecutionPolicy Bypass -File C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard\run_instagram_docker.ps1"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "Instagram Auto-Poster" -Trigger $trigger -Action $action -Principal $principal -Force
```

### 방법 2: 수동 실행

```powershell
cd "C:\Users\LG\Desktop\cursor pro+\while-you-were-sleeping-dashboard"
.\run_instagram_docker.ps1
```

---

## 📊 실행 흐름

```
매일 07:00 AM
↓
[run_daily_briefing.py]
├─ 화제 종목 조회
├─ 브리핑 생성 (이미지 생성)
├─ 📧 이메일 발송
└─ output/ 폴더 채움
   (약 5-10분 소요)

매일 07:30 AM
↓
[run_instagram_docker.ps1]
└─ Docker 컨테이너 실행
   └─ output/에서 이미지 읽음
   └─ 📱 인스타그램 게시
      (약 30초 소요)
```

---

## 🔍 확인

### 성공 확인

```powershell
# 1. Task Scheduler 확인
Get-ScheduledTask -TaskName "Instagram Auto-Poster"

# 2. 실행 이력
Get-ScheduledTaskInfo -TaskName "Instagram Auto-Poster"

# 3. 로그 확인
docker logs [container_id]
```

### Instagram 프로필 확인

1. Instagram 앱/웹 열기
2. 프로필 → 최신 포스트 확인
3. 캡션 확인: "📈 YYYY년 MM월 DD일 주식 브리핑"

---

## 🐳 자주 사용하는 Docker 명령어

```powershell
# 이미지 빌드
docker build -f Dockerfile.instagram -t instagram-poster .

# 이미지 목록
docker images | Select-String instagram

# 컨테이너 실행
docker run --rm -e INSTAGRAM_USERNAME=... instagram-poster

# 실행 중인 컨테이너
docker ps

# 모든 컨테이너
docker ps -a

# 로그 확인
docker logs [container_id]

# 컨테이너 정지
docker stop [container_id]

# 이미지 삭제
docker rmi instagram-poster
```

---

## ❌ 문제 해결

### "Docker daemon is not running"
→ Docker Desktop 실행

### "Cannot find image"
→ `docker build -f Dockerfile.instagram -t instagram-poster .` 실행

### "Permission denied"
→ PowerShell을 관리자 권한으로 실행

### "Cannot find .env"
→ `.env` 파일을 프로젝트 루트에 생성

### "No images found"
→ 먼저 `python -m services.briefing_generator` 실행

---

## 📚 전체 가이드

자세한 내용은 [DOCKER_INSTAGRAM_SETUP.md](DOCKER_INSTAGRAM_SETUP.md) 참조

---

**이제 Docker로 인스타그램 자동 게시가 시작됩니다! 🚀**

매일 07:30 AM에 자동 실행되며, Instagram 프로필에서 새 포스트를 확인할 수 있습니다.
