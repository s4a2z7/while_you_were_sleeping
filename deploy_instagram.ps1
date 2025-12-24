#!/usr/bin/env powershell
<#
인스타그램 자동 게시 배포 스크립트
Docker 사용
#>

# 색상 정의
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error_ { Write-Host $args -ForegroundColor Red }
function Write-Warning_ { Write-Host $args -ForegroundColor Yellow }
function Write-Info { Write-Host $args -ForegroundColor Cyan }

Write-Info "================================"
Write-Info "📱 인스타그램 자동 게시 배포"
Write-Info "================================"
Write-Info ""

# Step 1: Docker 확인
Write-Info "[1/5] Docker 설치 확인 중..."
$dockerCheck = docker --version 2>$null
if ($dockerCheck) {
    Write-Success "   ✅ Docker 설치됨: $dockerCheck"
} else {
    Write-Error_ "   ❌ Docker가 설치되지 않았습니다"
    Write-Info "   다운로드: https://www.docker.com/products/docker-desktop"
    exit 1
}

# Step 2: .env 파일 확인
Write-Info ""
Write-Info "[2/5] .env 파일 확인 중..."
$envFile = "backend\.env"
if (Test-Path $envFile) {
    $hasInstagram = Select-String "INSTAGRAM_USERNAME" $envFile -ErrorAction SilentlyContinue
    if ($hasInstagram) {
        Write-Success "   ✅ Instagram 설정 완료"
    } else {
        Write-Error_ "   ❌ INSTAGRAM_USERNAME이 설정되지 않았습니다"
        Write-Info "   backend\.env 파일을 수정하세요"
        exit 1
    }
} else {
    Write-Error_ "   ❌ .env 파일을 찾을 수 없습니다"
    exit 1
}

# Step 3: Dockerfile 확인
Write-Info ""
Write-Info "[3/5] Dockerfile 확인 중..."
if (Test-Path "Dockerfile.instagram") {
    Write-Success "   ✅ Dockerfile.instagram 찾음"
} else {
    Write-Error_ "   ❌ Dockerfile.instagram을 찾을 수 없습니다"
    exit 1
}

# Step 4: Docker 이미지 빌드
Write-Info ""
Write-Info "[4/5] Docker 이미지 빌드 중... (약 2-3분)"
Write-Warning_ "   ⚠️  Docker Desktop이 실행 중인지 확인하세요!"
Write-Info ""

docker build -f Dockerfile.instagram -t instagram-poster .

if ($LASTEXITCODE -eq 0) {
    Write-Success "   ✅ 이미지 빌드 성공"
} else {
    Write-Error_ "   ❌ 이미지 빌드 실패"
    Write-Warning_ "   Docker Desktop을 시작하고 다시 시도하세요"
    exit 1
}

# Step 5: 배포 완료
Write-Info ""
Write-Info "[5/5] 배포 준비 완료"
Write-Success "================================"
Write-Success "✅ 배포 완료!"
Write-Success "================================"
Write-Info ""
Write-Info "📱 다음 명령으로 인스타그램에 게시합니다:"
Write-Info ""
Write-Info "   .\run_instagram_docker.ps1"
Write-Info ""
Write-Info "🤖 또는 Task Scheduler로 자동 실행:"
Write-Info ""
Write-Info "   매일 07:30 AM에 자동 실행"
Write-Info ""
Write-Info "📚 자세한 가이드:"
Write-Info "   DOCKER_INSTAGRAM_QUICK_START.md"
Write-Info ""
